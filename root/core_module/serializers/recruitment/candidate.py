from core_module.models.recruitment.candidate import Candidate


class CandidateSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'full_name': obj.full_name,
            'email': obj.email,
            'phone': obj.phone,
            'applied_for_id': obj.applied_for_id,
            'applied_for_title': obj.applied_for.job_title if obj.applied_for else None,
            'source': obj.source,
            'source_display': obj.get_source_display() if obj.source else None,
            'current_stage': obj.current_stage,
            'current_stage_display': obj.get_current_stage_display(),
            'experience_yrs': str(obj.experience_yrs) if obj.experience_yrs else None,
            'current_salary': str(obj.current_salary) if obj.current_salary else None,
            'expected_salary': str(obj.expected_salary) if obj.expected_salary else None,
            'notice_period': obj.notice_period,
            'resume': obj.resume.url if obj.resume else None,
            'cover_letter': obj.cover_letter,
            'linkedin_url': obj.linkedin_url,
            'portfolio_url': obj.portfolio_url,
            'hired_employee_id': obj.hired_employee_id,
            'interview_count': obj.interviews.count(),
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [CandidateSerializer.serialize(obj) for obj in queryset]
