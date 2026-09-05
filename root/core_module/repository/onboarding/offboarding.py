from core_module.abstract.base_repository import BaseRepository
from core_module.models.onboarding.offboarding import OffboardingTask


class OffboardingTaskRepository(BaseRepository):
    def __init__(self):
        super().__init__(OffboardingTask)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def get_pending_tasks(self):
        return self.model.objects.filter(status='pending')
