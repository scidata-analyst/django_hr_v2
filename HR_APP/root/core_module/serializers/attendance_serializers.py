from core_module.models.attendance.attendance import Shift, Attendance, LeaveRequest


class ShiftSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'shift_name': obj.shift_name,
            'shift_code': obj.shift_code,
            'start_time': obj.start_time.strftime('%H:%M'),
            'end_time': obj.end_time.strftime('%H:%M'),
            'break_duration': obj.break_duration,
            'grace_period': obj.grace_period,
            'department_id': obj.department_id,
            'department_name': obj.department.name if obj.department else 'All Departments',
            'working_days': obj.working_days,
            'working_days_display': obj.get_working_days_display(),
            'overtime_eligible': obj.overtime_eligible,
            'is_active': obj.is_active,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [ShiftSerializer.serialize(obj) for obj in queryset]


class AttendanceSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'employee_id': obj.employee_id,
            'employee_name': obj.employee.full_name,
            'employee_code': obj.employee.employee_id,
            'date': obj.date.isoformat(),
            'check_in_time': obj.check_in_time.strftime('%H:%M') if obj.check_in_time else None,
            'check_out_time': obj.check_out_time.strftime('%H:%M') if obj.check_out_time else None,
            'total_hours': obj.total_hours,
            'status': obj.status,
            'status_display': obj.get_status_display(),
            'shift_id': obj.shift_id,
            'shift_name': obj.shift.shift_name if obj.shift else None,
            'overtime_hours': str(obj.overtime_hours),
            'work_location': obj.work_location,
            'work_location_display': obj.get_work_location_display(),
            'remarks': obj.remarks,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [AttendanceSerializer.serialize(obj) for obj in queryset]


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
