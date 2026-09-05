from core_module.models.attendance.leave import LeaveRequest


class LeaveRequestSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'employee_id': obj.employee_id,
            'employee_name': obj.employee.full_name,
            'employee_code': obj.employee.employee_id,
            'leave_type': obj.leave_type,
            'leave_type_display': obj.get_leave_type_display(),
            'from_date': obj.from_date.isoformat(),
            'to_date': obj.to_date.isoformat(),
            'total_days': obj.total_days,
            'reason': obj.reason,
            'document_attachment': obj.document_attachment.url if obj.document_attachment else None,
            'status': obj.status,
            'status_display': obj.get_status_display(),
            'approved_by_id': obj.approved_by_id,
            'approved_by_name': obj.approved_by.full_name if obj.approved_by else None,
            'approved_at': obj.approved_at.isoformat() if obj.approved_at else None,
            'denial_reason': obj.denial_reason,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [LeaveRequestSerializer.serialize(obj) for obj in queryset]
