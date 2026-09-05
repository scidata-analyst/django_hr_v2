from core_module.abstract.base_service import BaseService
from core_module.repository.recruitment.interview import InterviewRepository


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
