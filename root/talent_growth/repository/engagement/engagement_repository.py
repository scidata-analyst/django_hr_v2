from django.db.models import Avg, Count
from core_module.abstract.base_repository import BaseRepository
from talent_growth.models.talent_growth.talent_growth import (
    EngagementSurvey, SurveyResponse, SurveyQuestion, Recognition
)


class EngagementSurveyRepository(BaseRepository):
    def __init__(self):
        super().__init__(EngagementSurvey)

    def get_active_surveys(self):
        return self.model.objects.filter(is_active=True)


class SurveyResponseRepository(BaseRepository):
    def __init__(self):
        super().__init__(SurveyResponse)

    def get_by_survey(self, survey_id):
        return self.model.objects.filter(survey_id=survey_id)

    def get_average_score(self, survey_id):
        return self.model.objects.filter(survey_id=survey_id).aggregate(
            avg=Avg('overall_score')
        )['avg']


class RecognitionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Recognition)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def get_recent(self, limit=10):
        return self.model.objects.all()[:limit]

    def get_total_points(self, employee_id):
        from django.db.models import Sum
        return self.model.objects.filter(employee_id=employee_id).aggregate(
            total=Sum('points')
        )['total'] or 0
