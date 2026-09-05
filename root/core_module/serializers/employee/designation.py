from core_module.models.employee.designation import Designation


class DesignationSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'title': obj.title,
            'department_id': obj.department_id,
            'department_name': obj.department.name if obj.department else None,
            'level': obj.level,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [DesignationSerializer.serialize(obj) for obj in queryset]
