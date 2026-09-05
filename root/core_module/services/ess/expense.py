from core_module.abstract.base_service import BaseService
from core_module.repository.ess.ess_repository import ExpenseClaimRepository


class ExpenseClaimService(BaseService):
    def __init__(self):
        super().__init__(ExpenseClaimRepository())

    def submit_claim(self, data):
        return self.repository.create(**data), {}

    def approve_claim(self, claim_id, approved_by_id):
        from django.utils import timezone
        claim = self.repository.update(
            claim_id, status='approved', approved_by_id=approved_by_id,
            approved_at=timezone.now()
        )
        if claim is None:
            return None, {'error': 'Claim not found'}
        return claim, {}

    def reject_claim(self, claim_id, approved_by_id, rejection_reason=''):
        claim = self.repository.update(
            claim_id, status='rejected', approved_by_id=approved_by_id,
            rejection_reason=rejection_reason
        )
        if claim is None:
            return None, {'error': 'Claim not found'}
        return claim, {}

    def get_pending_claims(self):
        return self.repository.get_pending_claims()

    def get_by_employee(self, employee_id):
        return self.repository.get_by_employee(employee_id)
