from core_module.models.attendance.shift import Shift


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
