from core_module.models.onboarding.exit_interview import ExitInterview


class ExitInterviewSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'employee_id': obj.employee_id,
            'employee_name': obj.employee.full_name,
            'interviewer_id': obj.interviewer_id,
            'interviewer_name': obj.interviewer.full_name if obj.interviewer else None,
            'interview_date': obj.interview_date.isoformat(),
            'reason_for_leaving': obj.reason_for_leaving,
            'feedback': obj.feedback,
            'would_recommend': obj.would_recommend,
            'rating': obj.rating,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [ExitInterviewSerializer.serialize(obj) for obj in queryset]
