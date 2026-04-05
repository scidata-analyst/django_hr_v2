from django.db.models import Q, Count
from core_module.abstract.base_repository import BaseRepository
from core_module.models.recruitment.recruitment import JobPosting, Candidate, Interview


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


class CandidateRepository(BaseRepository):
    def __init__(self):
        super().__init__(Candidate)

    def get_by_job(self, job_posting_id):
        return self.model.objects.filter(applied_for_id=job_posting_id)

    def get_by_stage(self, stage):
        return self.model.objects.filter(current_stage=stage)

    def get_pipeline_summary(self):
        return self.model.objects.values('current_stage').annotate(count=Count('id'))

    def search_candidates(self, query):
        return self.search(['full_name', 'email'], query)

    def advance_stage(self, candidate_id):
        stage_order = ['applied', 'screening', 'interview', 'offer', 'hired']
        candidate = self.read(candidate_id)
        if candidate and candidate.current_stage in stage_order:
            current_idx = stage_order.index(candidate.current_stage)
            if current_idx < len(stage_order) - 1:
                candidate.current_stage = stage_order[current_idx + 1]
                candidate.save()
                return candidate
        return None


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
