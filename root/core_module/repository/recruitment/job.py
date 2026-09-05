from django.db.models import Count
from core_module.abstract.base_repository import BaseRepository
from core_module.models.recruitment.recruitment import JobPosting


class JobPostingRepository(BaseRepository):
    def __init__(self):
        super().__init__(JobPosting)

    def get_active_jobs(self):
        return self.model.objects.filter(status='active')

    def get_by_department(self, department_id):
        return self.model.objects.filter(department_id=department_id)

    def search_jobs(self, query):
        return self.search(['job_title', 'job_description', 'skills_required'], query)

    def get_by_status(self, status):
        return self.model.objects.filter(status=status)

    def get_with_candidate_count(self):
        return self.model.objects.annotate(candidate_count=Count('candidates'))
