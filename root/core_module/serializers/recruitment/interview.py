from core_module.models.recruitment.interview import Interview


class InterviewSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'candidate_id': obj.candidate_id,
            'candidate_name': obj.candidate.full_name,
            'interview_type': obj.interview_type,
            'interview_type_display': obj.get_interview_type_display(),
            'scheduled_at': obj.scheduled_at.isoformat(),
            'duration_mins': obj.duration_mins,
            'interviewer_id': obj.interviewer_id,
            'interviewer_name': obj.interviewer.full_name if obj.interviewer else None,
            'location': obj.location,
            'meeting_link': obj.meeting_link,
            'result': obj.result,
            'result_display': obj.get_result_display(),
            'feedback': obj.feedback,
            'rating': obj.rating,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [InterviewSerializer.serialize(obj) for obj in queryset]
