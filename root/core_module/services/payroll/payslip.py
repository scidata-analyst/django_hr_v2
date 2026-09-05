from decimal import Decimal
from core_module.abstract.base_service import BaseService
from core_module.repository.payroll.payslip import PayslipRepository


class PayslipService(BaseService):
    def __init__(self):
        super().__init__(PayslipRepository())

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
