from core_module.abstract.base_repository import BaseRepository
from core_module.models.payroll.loan import Loan, LoanRepayment


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
