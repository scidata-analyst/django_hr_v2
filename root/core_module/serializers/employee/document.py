from core_module.models.employee.document import Document


class DocumentSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'employee_id': obj.employee_id,
            'employee_name': obj.employee.full_name,
            'document_type': obj.document_type,
            'document_type_display': obj.get_document_type_display(),
            'title': obj.title,
            'file': obj.file.url if obj.file else None,
            'status': obj.status,
            'status_display': obj.get_status_display(),
            'expiry_date': obj.expiry_date.isoformat() if obj.expiry_date else None,
            'notes': obj.notes,
            'uploaded_at': obj.uploaded_at.isoformat(),
            'verified_at': obj.verified_at.isoformat() if obj.verified_at else None,
        }

    @staticmethod
    def serialize_list(queryset):
        return [DocumentSerializer.serialize(obj) for obj in queryset]
