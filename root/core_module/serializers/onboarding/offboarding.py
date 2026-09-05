from core_module.models.onboarding.offboarding import OffboardingTask


class OffboardingTaskSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'employee_id': obj.employee_id,
            'employee_name': obj.employee.full_name,
            'task_type': obj.task_type,
            'task_type_display': obj.get_task_type_display(),
            'task_name': obj.task_name,
            'description': obj.description,
            'assigned_to_id': obj.assigned_to_id,
            'assigned_to_name': obj.assigned_to.full_name if obj.assigned_to else None,
            'due_date': obj.due_date.isoformat() if obj.due_date else None,
            'completed_date': obj.completed_date.isoformat() if obj.completed_date else None,
            'status': obj.status,
            'status_display': obj.get_status_display(),
            'notes': obj.notes,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [OffboardingTaskSerializer.serialize(obj) for obj in queryset]
