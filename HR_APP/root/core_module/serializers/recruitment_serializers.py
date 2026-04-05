from core_module.models.recruitment.recruitment import JobPosting, Candidate, Interview


class JobPostingSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'job_title': obj.job_title,
            'department_id': obj.department_id,
            'department_name': obj.department.name if obj.department else None,
            'job_type': obj.job_type,
            'job_type_display': obj.get_job_type_display(),
            'location_id': obj.location_id,
            'location_name': obj.location.name if obj.location else None,
            'salary_range_min': str(obj.salary_range_min) if obj.salary_range_min else None,
            'salary_range_max': str(obj.salary_range_max) if obj.salary_range_max else None,
            'vacancies': obj.vacancies,
            'application_deadline': obj.application_deadline.isoformat() if obj.application_deadline else None,
            'experience_required': obj.experience_required,
            'education_level': obj.education_level,
            'job_description': obj.job_description,
            'skills_required': obj.skills_required,
            'publish_on': obj.publish_on,
            'status': obj.status,
            'status_display': obj.get_status_display(),
            'candidate_count': obj.candidates.count(),
            'created_by_id': obj.created_by_id,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [JobPostingSerializer.serialize(obj) for obj in queryset]


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
