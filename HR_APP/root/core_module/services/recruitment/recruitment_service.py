from core_module.abstract.base_service import BaseService
from core_module.repository.recruitment.recruitment_repository import (
    JobPostingRepository, CandidateRepository, InterviewRepository
)


class JobPostingService(BaseService):
    def __init__(self):
        super().__init__(JobPostingRepository())

    def get_active_jobs(self):
        return self.repository.get_active_jobs()

    def search_jobs(self, query):
        return self.repository.search_jobs(query)


class CandidateService(BaseService):
    def __init__(self):
        super().__init__(CandidateRepository())

    def advance_stage(self, candidate_id):
        candidate = self.repository.advance_stage(candidate_id)
        if candidate is None:
            return None, {'error': 'Cannot advance candidate stage'}
        return candidate, {}

    def reject_candidate(self, candidate_id):
        candidate = self.repository.update(candidate_id, current_stage='rejected')
        if candidate is None:
            return None, {'error': 'Candidate not found'}
        return candidate, {}

    def get_pipeline_summary(self):
        return self.repository.get_pipeline_summary()

    def get_by_stage(self, stage):
        return self.repository.get_by_stage(stage)


class InterviewService(BaseService):
    def __init__(self):
        super().__init__(InterviewRepository())

    def schedule_interview(self, data):
        return self.repository.create(**data), {}

    def submit_result(self, interview_id, result, feedback='', rating=None):
        interview = self.repository.update(
            interview_id, result=result, feedback=feedback, rating=rating
        )
        if interview is None:
            return None, {'error': 'Interview not found'}
        return interview, {}

    def get_upcoming(self):
        return self.repository.get_upcoming()
