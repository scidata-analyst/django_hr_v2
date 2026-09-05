from core_module.models.recruitment.job import JobPosting


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
