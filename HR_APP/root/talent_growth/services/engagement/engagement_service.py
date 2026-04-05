from core_module.abstract.base_service import BaseService
from talent_growth.repository.engagement.engagement_repository import (
    EngagementSurveyRepository, SurveyResponseRepository, RecognitionRepository
)


class EngagementSurveyService(BaseService):
    def __init__(self):
        super().__init__(EngagementSurveyRepository())

    def create_survey(self, data):
        questions = data.pop('questions', [])
        survey = self.repository.create(**data)
        from talent_growth.models.talent_growth.talent_growth import SurveyQuestion
        for i, q_text in enumerate(questions):
            SurveyQuestion.objects.create(
                survey=survey, question_text=q_text, question_type='rating', order=i
            )
        return survey, {}

    def get_active_surveys(self):
        return self.repository.get_active_surveys()


class SurveyResponseService(BaseService):
    def __init__(self):
        super().__init__(SurveyResponseRepository())

    def submit_response(self, data):
        return self.repository.create(**data), {}


class RecognitionService(BaseService):
    def __init__(self):
        super().__init__(RecognitionRepository())

    def recognize_employee(self, data):
        return self.repository.create(**data), {}

    def get_by_employee(self, employee_id):
        return self.repository.get_by_employee(employee_id)

    def get_total_points(self, employee_id):
        return self.repository.get_total_points(employee_id)

    def get_recent(self, limit=10):
        return self.repository.get_recent(limit)
