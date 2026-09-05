from core_module.models.employee.department import Department


class DepartmentSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'description': obj.description,
            'employee_count': getattr(obj, 'employee_count', obj.employee_set.count()),
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [DepartmentSerializer.serialize(obj) for obj in queryset]
