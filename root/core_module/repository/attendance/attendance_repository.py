from django.db.models import Q, Count, Sum
from core_module.abstract.base_repository import BaseRepository
from core_module.models.attendance.attendance import Shift, Attendance, LeaveRequest


class ShiftRepository(BaseRepository):
    def __init__(self):
        super().__init__(Shift)

    def get_active_shifts(self):
        return self.model.objects.filter(is_active=True)

    def get_by_department(self, department_id):
        return self.model.objects.filter(
            Q(department_id=department_id) | Q(department__isnull=True)
        )


class AttendanceRepository(BaseRepository):
    def __init__(self):
        super().__init__(Attendance)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def get_by_date(self, date):
        return self.model.objects.filter(date=date)

    def get_by_date_range(self, start_date, end_date):
        return self.model.objects.filter(date__gte=start_date, date__lte=end_date)

    def get_by_employee_and_date_range(self, employee_id, start_date, end_date):
        return self.model.objects.filter(
            employee_id=employee_id, date__gte=start_date, date__lte=end_date
        )

    def get_present_today(self, date):
        return self.model.objects.filter(date=date, status='present')

    def get_attendance_summary(self, start_date, end_date):
        return self.model.objects.filter(
            date__gte=start_date, date__lte=end_date
        ).values('status').annotate(count=Count('id'))

    def get_employee_attendance_stats(self, employee_id, start_date, end_date):
        records = self.model.objects.filter(
            employee_id=employee_id, date__gte=start_date, date__lte=end_date
        )
        return {
            'total_days': records.count(),
            'present': records.filter(status='present').count(),
            'absent': records.filter(status='absent').count(),
            'late': records.filter(status='late').count(),
            'half_day': records.filter(status='half_day').count(),
            'on_leave': records.filter(status='on_leave').count(),
            'work_from_home': records.filter(status='work_from_home').count(),
            'total_overtime': records.aggregate(total=Sum('overtime_hours'))['total'] or 0,
        }


class LeaveRequestRepository(BaseRepository):
    def __init__(self):
        super().__init__(LeaveRequest)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def get_pending_requests(self):
        return self.model.objects.filter(status='pending')

    def get_by_status(self, status):
        return self.model.objects.filter(status=status)

    def check_overlapping_leave(self, employee_id, from_date, to_date, exclude_id=None):
        qs = self.model.objects.filter(
            employee_id=employee_id, status='approved',
            from_date__lte=to_date, to_date__gte=from_date
        )
        if exclude_id:
            qs = qs.exclude(pk=exclude_id)
        return qs.exists()
