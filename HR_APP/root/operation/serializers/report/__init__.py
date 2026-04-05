from operation.models.report.report import Report


class ReportSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'report_name': instance.report_name,
            'report_type': instance.report_type,
            'description': instance.description,
            'parameters': instance.parameters,
            'created_by': instance.created_by.full_name if instance.created_by else None,
            'created_at': str(instance.created_at),
        }

    @staticmethod
    def serialize_list(qs):
        return [ReportSerializer.serialize(obj) for obj in qs]
