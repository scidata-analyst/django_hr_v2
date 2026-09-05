from core_module.models.employee.location import Location


class LocationSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'city': obj.city,
            'country': obj.country,
            'location_type': obj.location_type,
            'location_type_display': obj.get_location_type_display(),
            'is_active': obj.is_active,
            'employee_count': getattr(obj, 'employee_count', obj.employee_set.count()),
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [LocationSerializer.serialize(obj) for obj in queryset]
