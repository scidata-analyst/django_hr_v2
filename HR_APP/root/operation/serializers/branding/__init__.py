from operation.models.health.health import SafetyIncident


class AuditLogSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'action': getattr(instance, 'action', ''),
            'user': getattr(instance, 'user', None),
            'timestamp': str(getattr(instance, 'timestamp', '')),
        }

    @staticmethod
    def serialize_list(qs):
        return [AuditLogSerializer.serialize(obj) for obj in qs]
