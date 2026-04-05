from django.db.models import Q
from core_module.abstract.base_repository import BaseRepository
from operation.models.operation.operation import (
    PolicyDocument, PolicyAcknowledgement, ComplianceChecklist
)


class PolicyDocumentRepository(BaseRepository):
    def __init__(self):
        super().__init__(PolicyDocument)

    def get_by_category(self, category):
        return self.model.objects.filter(category=category)

    def get_mandatory_policies(self):
        return self.model.objects.filter(is_mandatory=True)

    def search_policies(self, query):
        return self.model.objects.filter(
            Q(policy_name__icontains=query) |
            Q(category__icontains=query) |
            Q(description__icontains=query)
        )


class PolicyAcknowledgementRepository(BaseRepository):
    def __init__(self):
        super().__init__(PolicyAcknowledgement)

    def get_by_policy(self, policy_id):
        return self.model.objects.filter(policy_id=policy_id)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def acknowledge(self, policy_id, employee_id):
        obj, created = self.model.objects.get_or_create(
            policy_id=policy_id, employee_id=employee_id
        )
        return obj, created


class ComplianceChecklistRepository(BaseRepository):
    def __init__(self):
        super().__init__(ComplianceChecklist)

    def get_pending(self):
        return self.model.objects.filter(status='pending')

    def get_by_category(self, category):
        return self.model.objects.filter(category=category)

    def get_by_status(self, status):
        return self.model.objects.filter(status=status)
