from datetime import date, timedelta
from django.db import IntegrityError
from django.db.models import Count, Q, Sum
from core_module.abstract.base_service import BaseService
from core_module.repository.attendance.attendance_repository import (
    ShiftRepository, AttendanceRepository, LeaveRequestRepository
)
from core_module.models.attendance.attendance import Attendance, LeaveRequest


class ShiftService(BaseService):
    def __init__(self):
        super().__init__(ShiftRepository())

    def get_active_shifts(self):
        return self.repository.get_active_shifts()


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


class LeaveRequestService(BaseService):
    def __init__(self):
        super().__init__(LeaveRequestRepository())

    def validate(self, **kwargs):
        errors = {}
        from_date = kwargs.get('from_date')
        to_date = kwargs.get('to_date')
        if from_date and to_date and from_date > to_date:
            errors['to_date'] = 'To date must be after from date.'
        employee_id = kwargs.get('employee_id')
        if employee_id and from_date and to_date:
            if self.repository.check_overlapping_leave(
                employee_id, from_date, to_date, kwargs.get('pk')
            ):
                errors['date'] = 'Overlapping approved leave exists for these dates.'
        return len(errors) == 0, errors

    def apply_leave(self, data):
        is_valid, errors = self.validate(**data)
        if not is_valid:
            return None, errors
        try:
            leave = self.repository.create(**data)
            return leave, {}
        except IntegrityError as e:
            return None, {'error': str(e)}

    def approve_leave(self, leave_id, approved_by_id):
        leave = self.repository.read(leave_id)
        if not leave:
            return None, {'error': 'Leave request not found'}
        if leave.status != 'pending':
            return None, {'error': 'Leave request is not pending'}
        from django.utils import timezone
        leave.status = 'approved'
        leave.approved_by_id = approved_by_id
        leave.approved_at = timezone.now()
        leave.save()
        return leave, {}

    def deny_leave(self, leave_id, approved_by_id, denial_reason=''):
        leave = self.repository.read(leave_id)
        if not leave:
            return None, {'error': 'Leave request not found'}
        if leave.status != 'pending':
            return None, {'error': 'Leave request is not pending'}
        leave.status = 'denied'
        leave.approved_by_id = approved_by_id
        leave.denial_reason = denial_reason
        leave.save()
        return leave, {}

    def get_pending_requests(self):
        return self.repository.get_pending_requests()

    def get_by_employee(self, employee_id):
        return self.repository.get_by_employee(employee_id)
