from django.db.models import Count
from core_module.abstract.base_repository import BaseRepository
from core_module.models.recruitment.recruitment import Candidate


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
