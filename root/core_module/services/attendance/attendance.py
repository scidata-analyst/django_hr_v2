from datetime import date
from django.db.models import Count, Q
from core_module.abstract.base_service import BaseService
from core_module.repository.attendance.attendance_repository import AttendanceRepository
from core_module.models.attendance.attendance import Attendance


class AttendanceService(BaseService):
    def __init__(self):
        super().__init__(AttendanceRepository())

    def validate(self, **kwargs):
        errors = {}
        employee_id = kwargs.get('employee_id')
        att_date = kwargs.get('date')
        if employee_id and att_date:
            if Attendance.objects.filter(
                employee_id=employee_id, date=att_date
            ).exclude(pk=kwargs.get('pk')).exists():
                errors['date'] = 'Attendance already marked for this employee on this date.'
        check_in = kwargs.get('check_in_time')
        check_out = kwargs.get('check_out_time')
        if check_in and check_out and check_in == check_out:
            errors['check_out_time'] = 'Check-out time cannot be identical to check-in time.'
        return len(errors) == 0, errors

    def mark_attendance(self, data):
        from django.db import IntegrityError
        is_valid, errors = self.validate(**data)
        if not is_valid:
            return None, errors
        try:
            attendance = self.repository.create(**data)
            return attendance, {}
        except IntegrityError:
            return None, {'error': 'Attendance already marked for this date'}

    def get_today_attendance(self):
        today = date.today()
        return self.repository.get_by_date(today)

    def get_attendance_stats(self, start_date=None, end_date=None):
        if not start_date:
            start_date = date.today()
        if not end_date:
            end_date = date.today()
        records = self.repository.get_by_date_range(start_date, end_date)
        agg = records.aggregate(
            total_records=Count('id'),
            present=Count('id', filter=Q(status='present')),
            absent=Count('id', filter=Q(status='absent')),
            late=Count('id', filter=Q(status='late')),
            half_day=Count('id', filter=Q(status='half_day')),
            on_leave=Count('id', filter=Q(status='on_leave')),
            work_from_home=Count('id', filter=Q(status='work_from_home')),
        )
        return agg

    def get_employee_stats(self, employee_id, start_date=None, end_date=None):
        if not start_date:
            start_date = date.today().replace(day=1)
        if not end_date:
            end_date = date.today()
        return self.repository.get_employee_attendance_stats(employee_id, start_date, end_date)
