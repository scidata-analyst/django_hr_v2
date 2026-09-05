from core_module.abstract.base_service import BaseService
from core_module.repository.recruitment.candidate import CandidateRepository


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
