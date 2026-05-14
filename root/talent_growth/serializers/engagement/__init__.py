from talent_growth.models.engagement.engagement import EngagementSurvey, SurveyQuestion, SurveyResponse, Recognition


class EngagementSurveySerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'title': instance.title,
            'description': instance.description,
            'start_date': str(instance.start_date),
            'end_date': str(instance.end_date),
            'is_anonymous': instance.is_anonymous,
            'is_active': instance.is_active,
        }

    @staticmethod
    def serialize_list(qs):
        return [EngagementSurveySerializer.serialize(obj) for obj in qs]


class SurveyQuestionSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'survey_id': instance.survey_id,
            'question_text': instance.question_text,
            'question_type': instance.question_type,
            'options': instance.options,
            'order': instance.order,
            'is_required': instance.is_required,
        }

    @staticmethod
    def serialize_list(qs):
        return [SurveyQuestionSerializer.serialize(obj) for obj in qs]


class SurveyResponseSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'survey_id': instance.survey_id,
            'employee': instance.employee.full_name if instance.employee else None,
            'submitted_at': str(instance.submitted_at),
            'overall_score': float(instance.overall_score) if instance.overall_score else None,
        }

    @staticmethod
    def serialize_list(qs):
        return [SurveyResponseSerializer.serialize(obj) for obj in qs]


class RecognitionSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'employee': instance.employee.full_name if instance.employee else None,
            'recognized_by': instance.recognized_by.full_name if instance.recognized_by else None,
            'recognition_type': instance.recognition_type,
            'reason': instance.reason,
            'points': instance.points,
            'given_at': str(instance.given_at),
        }

    @staticmethod
    def serialize_list(qs):
        return [RecognitionSerializer.serialize(obj) for obj in qs]
