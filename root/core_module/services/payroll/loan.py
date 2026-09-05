from core_module.abstract.base_service import BaseService
from core_module.repository.payroll.payroll_repository import LoanRepository


class LoanService(BaseService):
    def __init__(self):
        super().__init__(LoanRepository())

    def validate(self, **kwargs):
        errors = {}
        if kwargs.get('loan_amount') and kwargs['loan_amount'] <= 0:
            errors['loan_amount'] = 'Loan amount must be positive.'
        if kwargs.get('repayment_period') and kwargs['repayment_period'] <= 0:
            errors['repayment_period'] = 'Repayment period must be positive.'
        return len(errors) == 0, errors

    def create_loan(self, data):
        is_valid, errors = self.validate(**data)
        if not is_valid:
            return None, errors
        return self.repository.create(**data), {}

    def approve_loan(self, loan_id, approved_by_id):
        loan = self.repository.read(loan_id)
        if not loan:
            return None, {'error': 'Loan not found'}
        loan.status = 'active'
        loan.approved_by_id = approved_by_id
        from datetime import date
        loan.disbursement_date = date.today()
        loan.save()
        return loan, {}

    def get_active_loans(self):
        return self.repository.get_active_loans()
