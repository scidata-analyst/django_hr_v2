from core_module.abstract.base_repository import BaseRepository
from core_module.models.onboarding.onboarding import ExitInterview


class ExitInterviewRepository(BaseRepository):
    def __init__(self):
        super().__init__(ExitInterview)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def get_by_interviewer(self, employee_id):
        return self.model.objects.filter(interviewer_id=employee_id)
