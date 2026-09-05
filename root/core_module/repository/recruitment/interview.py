from core_module.abstract.base_repository import BaseRepository
from core_module.models.recruitment.interview import Interview


class InterviewRepository(BaseRepository):
    def __init__(self):
        super().__init__(Interview)

    def get_by_candidate(self, candidate_id):
        return self.model.objects.filter(candidate_id=candidate_id)

    def get_upcoming(self):
        from django.utils import timezone
        return self.model.objects.filter(scheduled_at__gte=timezone.now()).order_by('scheduled_at')

    def get_by_interviewer(self, employee_id):
        return self.model.objects.filter(interviewer_id=employee_id)
