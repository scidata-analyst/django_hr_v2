from django.db.models import Sum, Q
from core_module.abstract.base_repository import BaseRepository
from core_module.models.payroll.payroll import SalaryStructure, Payslip, Loan, LoanRepayment, Bonus


class SalaryStructureRepository(BaseRepository):
    def __init__(self):
        super().__init__(SalaryStructure)

    def get_active(self):
        return self.model.objects.filter(is_active=True)


class PayslipRepository(BaseRepository):
    def __init__(self):
        super().__init__(Payslip)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def get_by_period(self, pay_period):
        return self.model.objects.filter(pay_period=pay_period)

    def get_by_employee_and_period(self, employee_id, pay_period):
        try:
            return self.model.objects.get(employee_id=employee_id, pay_period=pay_period)
        except self.model.DoesNotExist:
            return None

    def get_payroll_summary(self, pay_period):
        payslips = self.model.objects.filter(pay_period=pay_period)
        return {
            'total_employees': payslips.count(),
            'total_gross': payslips.aggregate(total=Sum('basic_salary'))['total'] or 0,
            'total_deductions': payslips.aggregate(
                total=Sum('income_tax') + Sum('provident_fund') + Sum('insurance_deduction')
            )['total'] or 0,
        }


class LoanRepository(BaseRepository):
    def __init__(self):
        super().__init__(Loan)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def get_active_loans(self):
        return self.model.objects.filter(status='active')

    def get_pending_loans(self):
        return self.model.objects.filter(status='pending')


class LoanRepaymentRepository(BaseRepository):
    def __init__(self):
        super().__init__(LoanRepayment)

    def get_by_loan(self, loan_id):
        return self.model.objects.filter(loan_id=loan_id)


class BonusRepository(BaseRepository):
    def __init__(self):
        super().__init__(Bonus)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def get_by_month(self, pay_month):
        return self.model.objects.filter(pay_month=pay_month)

    def get_pending_bonuses(self):
        return self.model.objects.filter(status='pending')
