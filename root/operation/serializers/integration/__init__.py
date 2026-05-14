from operation.models.integration.integration import Integration


class IntegrationSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'integration_type': instance.integration_type,
            'is_enabled': instance.is_enabled,
            'status': instance.status,
            'last_sync': str(instance.last_sync) if instance.last_sync else None,
            'settings': instance.settings,
        }

    @staticmethod
    def serialize_list(qs):
        return [IntegrationSerializer.serialize(obj) for obj in qs]
