from core_module.abstract.base_service import BaseService
from operation.repository.compliance_repository import (
    PolicyDocumentRepository, PolicyAcknowledgementRepository, ComplianceChecklistRepository
)


class PolicyDocumentService(BaseService):
    def __init__(self):
        super().__init__(PolicyDocumentRepository())

    def get_mandatory_policies(self):
        return self.repository.get_mandatory_policies()


class PolicyAcknowledgementService(BaseService):
    def __init__(self):
        super().__init__(PolicyAcknowledgementRepository())

    def acknowledge_policy(self, policy_id, employee_id):
        obj, created = self.repository.acknowledge(policy_id, employee_id)
        return obj, {'is_new': created}

    def get_by_policy(self, policy_id):
        return self.repository.get_by_policy(policy_id)


class ComplianceChecklistService(BaseService):
    def __init__(self):
        super().__init__(ComplianceChecklistRepository())

    def get_pending(self):
        return self.repository.get_pending()

    def complete_item(self, checklist_id, notes=''):
        from django.utils import timezone
        item = self.repository.update(
            checklist_id, status='completed',
            notes=notes, completed_at=timezone.now()
        )
        if item is None:
            return None, {'error': 'Checklist item not found'}
        return item, {}
