from core_module.abstract.base_service import BaseService
from operation.repository.report_repository import ReportRepository


class ReportService(BaseService):
    def __init__(self):
        super().__init__(ReportRepository())

    def generate_headcount_report(self):
        from core_module.models.employee.employee import Employee
        from django.db.models import Count
        return list(
            Employee.objects.filter(status='active')
            .values('department__name')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

    def generate_attendance_report(self, start_date, end_date):
        from core_module.models.attendance.attendance import Attendance
        from django.db.models import Count
        return list(
            Attendance.objects.filter(date__gte=start_date, date__lte=end_date)
            .values('status')
            .annotate(count=Count('id'))
        )

    def generate_turnover_report(self):
        from core_module.models.employee.employee import Employee
        from datetime import date, timedelta
        one_year_ago = date.today() - timedelta(days=365)
        resigned = Employee.objects.filter(
            resignation_date__gte=one_year_ago
        ).count()
        total = Employee.objects.count()
        return {
            'resigned_last_year': resigned,
            'total_employees': total,
            'turnover_rate': round(resigned / total * 100, 2) if total > 0 else 0,
        }
