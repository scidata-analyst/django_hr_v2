from operation.models.global_.global_ import Office


class OfficeSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'country': instance.country,
            'city': instance.city,
            'office_type': instance.office_type,
            'full_address': instance.full_address,
            'local_currency': instance.local_currency,
            'timezone': instance.timezone,
            'capacity': instance.capacity,
            'status': instance.status,
        }

    @staticmethod
    def serialize_list(qs):
        return [OfficeSerializer.serialize(obj) for obj in qs]
