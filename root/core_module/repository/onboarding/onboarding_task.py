from core_module.abstract.base_repository import BaseRepository
from core_module.models.onboarding.onboarding import OnboardingTask


class OnboardingTaskRepository(BaseRepository):
    def __init__(self):
        super().__init__(OnboardingTask)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def get_pending_tasks(self):
        return self.model.objects.filter(status='pending')

    def get_by_status(self, status):
        return self.model.objects.filter(status=status)

    def get_in_progress(self):
        return self.model.objects.filter(status='in_progress')

    def search_tasks(self, query):
        return self.search(['employee_name', 'task_name'], query)
