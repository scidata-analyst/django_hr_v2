from core_module.abstract.base_service import BaseService
from operation.repository.safety_repository import SafetyIncidentRepository


class SafetyIncidentService(BaseService):
    def __init__(self):
        super().__init__(SafetyIncidentRepository())

    def report_incident(self, data):
        return self.repository.create(**data), {}

    def resolve_incident(self, incident_id, corrective_action=''):
        from django.utils import timezone
        incident = self.repository.update(
            incident_id, status='resolved',
            corrective_action=corrective_action,
            resolved_at=timezone.now()
        )
        if incident is None:
            return None, {'error': 'Incident not found'}
        return incident, {}

    def get_open_incidents(self):
        return self.repository.get_open_incidents()
