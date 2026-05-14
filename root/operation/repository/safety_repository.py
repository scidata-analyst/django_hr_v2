from core_module.abstract.base_repository import BaseRepository
from operation.models.operation.operation import SafetyIncident


class SafetyIncidentRepository(BaseRepository):
    def __init__(self):
        super().__init__(SafetyIncident)

    def get_open_incidents(self):
        return self.model.objects.filter(status__in=['reported', 'investigating'])

    def get_by_severity(self, severity):
        return self.model.objects.filter(severity=severity)

    def get_by_reporter(self, employee_id):
        return self.model.objects.filter(reported_by_id=employee_id)
