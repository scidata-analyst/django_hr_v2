from core_module.models.attendance.attendance import Attendance


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
