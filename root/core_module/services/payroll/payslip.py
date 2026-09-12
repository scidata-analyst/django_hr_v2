from decimal import Decimal
from django.db.models import Sum, Count, F, Q
from core_module.abstract.base_service import BaseService
from core_module.repository.payroll.payslip import PayslipRepository


class PayslipService(BaseService):
    def __init__(self):
        super().__init__(PayslipRepository())

    def get_payroll_stats(self, pay_period=None):
        """Aggregated payroll stats like attendance_stats. Returns gross, deductions, net, bonuses."""
        qs = self.get_all()
        if pay_period:
            qs = qs.filter(pay_period__icontains=pay_period)

        gross_fields = [
            'basic_salary', 'house_rent', 'transport_allowance',
            'medical_allowance', 'food_allowance', 'other_allowance',
            'overtime_amount', 'bonus_amount'
        ]
        deduction_fields = [
            'income_tax', 'provident_fund', 'insurance_deduction',
            'other_deductions', 'loan_emi', 'absent_deduction', 'late_deduction'
        ]
        all_fields = gross_fields + deduction_fields
        aggregations = qs.aggregate(**{f"sum_{f}": Sum(f) for f in all_fields})
        total_gross = sum(float(aggregations.get(f"sum_{f}") or 0) for f in gross_fields)
        total_deductions = sum(float(aggregations.get(f"sum_{f}") or 0) for f in deduction_fields)
        net_payroll = total_gross - total_deductions

        # Bonuses aggregation (optionally filter by pay_period if it looks like a month string)
        from core_module.models.payroll.bonus import Bonus
        bonus_qs = Bonus.objects.all()
        # If pay_period contains year/month, try to filter bonuses by same year-month substring in pay_month?
        # Keep simple: no filter unless pay_period matches bonus pay_month year-month
        # For now, aggregate all bonuses
        bonus_agg = bonus_qs.aggregate(total=Sum('amount'), count=Count('id'))
        total_bonuses = float(bonus_agg['total'] or 0)
        bonus_count = bonus_agg['count'] or 0

        # Active loans
        from core_module.models.payroll.loan import Loan
        loan_qs = Loan.objects.filter(status='active')
        loan_agg = loan_qs.aggregate(total=Sum('loan_amount'), count=Count('id'))
        active_loans_total = float(loan_agg['total'] or 0)
        active_loans_count = loan_agg['count'] or 0

        payslip_count = qs.count()

        return {
            'gross_payroll': round(total_gross, 2),
            'total_deductions': round(total_deductions, 2),
            'net_payroll': round(net_payroll, 2),
            'total_bonuses': round(total_bonuses, 2),
            'payslip_count': payslip_count,
            'bonus_count': bonus_count,
            'active_loans_count': active_loans_count,
            'active_loans_total': round(active_loans_total, 2),
            'pay_period': pay_period or '',
        }

    def get_breakdown_by_department(self, pay_period=None):
        """Salary breakdown grouped by employee department."""
        qs = self.get_all().select_related('employee__department')
        if pay_period:
            qs = qs.filter(pay_period__icontains=pay_period)

        # values + annotate grouping
        breakdown = qs.values(dept_name=F('employee__department__name')).annotate(
            employees=Count('id'),
            total_basic=Sum('basic_salary'),
            total_house_rent=Sum('house_rent'),
            total_transport=Sum('transport_allowance'),
            total_medical=Sum('medical_allowance'),
            total_food=Sum('food_allowance'),
            total_other_allowance=Sum('other_allowance'),
            total_overtime=Sum('overtime_amount'),
            total_bonus=Sum('bonus_amount'),
            total_income_tax=Sum('income_tax'),
            total_pf=Sum('provident_fund'),
            total_insurance=Sum('insurance_deduction'),
            total_other_ded=Sum('other_deductions'),
            total_loan_emi=Sum('loan_emi'),
            total_absent=Sum('absent_deduction'),
            total_late=Sum('late_deduction'),
        ).order_by('dept_name')

        result = []
        for row in breakdown:
            dept = row['dept_name'] or 'Unassigned'
            basic = float(row['total_basic'] or 0)
            allowances = (
                float(row['total_house_rent'] or 0) +
                float(row['total_transport'] or 0) +
                float(row['total_medical'] or 0) +
                float(row['total_food'] or 0) +
                float(row['total_other_allowance'] or 0) +
                float(row['total_overtime'] or 0) +
                float(row['total_bonus'] or 0)
            )
            deductions = (
                float(row['total_income_tax'] or 0) +
                float(row['total_pf'] or 0) +
                float(row['total_insurance'] or 0) +
                float(row['total_other_ded'] or 0) +
                float(row['total_loan_emi'] or 0) +
                float(row['total_absent'] or 0) +
                float(row['total_late'] or 0)
            )
            gross = basic + allowances
            net = gross - deductions
            result.append({
                'department': dept,
                'employees': row['employees'],
                'basic_salary': round(basic, 2),
                'allowances': round(allowances, 2),
                'deductions': round(deductions, 2),
                'gross': round(gross, 2),
                'net_pay': round(net, 2),
                'status': 'Processed' if row['employees'] > 0 else 'Pending',
            })
        return result

    def generate_payslip(self, employee, pay_period, pay_date):
        from core_module.models.payroll.payslip import Payslip
        if self.repository.get_by_employee_and_period(employee.id, pay_period):
            return None, {'error': f'Payslip already exists for {pay_period}'}
        basic = employee.basic_salary or Decimal('0')
        house_rent = basic * Decimal('0.20')
        transport = Decimal('100')
        medical = Decimal('80')
        food = Decimal('50')
        income_tax = basic * Decimal('0.10')
        pf = basic * Decimal('0.08')
        insurance = Decimal('30')
        gross = basic + house_rent + transport + medical + food
        total_ded = income_tax + pf + insurance
        net = gross - total_ded
        payslip = Payslip.objects.create(
            employee=employee, pay_period=pay_period, pay_date=pay_date,
            basic_salary=basic, house_rent=house_rent,
            transport_allowance=transport, medical_allowance=medical,
            food_allowance=food, income_tax=income_tax,
            provident_fund=pf, insurance_deduction=insurance,
            is_generated=True
        )
        return payslip, {}

    def bulk_generate(self, pay_period, pay_date):
        from core_module.models.employee.employee import Employee
        employees = Employee.objects.filter(status='active')
        results = {'generated': 0, 'skipped': 0, 'errors': []}
        for emp in employees:
            payslip, error = self.generate_payslip(emp, pay_period, pay_date)
            if payslip:
                results['generated'] += 1
            else:
                results['skipped'] += 1
                if error:
                    results['errors'].append({'employee': emp.full_name, **error})
        return results

    def get_by_employee(self, employee_id):
        return self.repository.get_by_employee(employee_id)
