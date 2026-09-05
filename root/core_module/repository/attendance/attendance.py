from django.db.models import Q, Count, Sum
from core_module.abstract.base_repository import BaseRepository
from core_module.models.attendance.attendance import Attendance


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
        agg = records.aggregate(
            total_days=Count('id'),
            present=Count('id', filter=Q(status='present')),
            absent=Count('id', filter=Q(status='absent')),
            late=Count('id', filter=Q(status='late')),
            half_day=Count('id', filter=Q(status='half_day')),
            on_leave=Count('id', filter=Q(status='on_leave')),
            work_from_home=Count('id', filter=Q(status='work_from_home')),
            total_overtime=Sum('overtime_hours'),
        )
        agg['total_overtime'] = agg['total_overtime'] or 0
        return agg
