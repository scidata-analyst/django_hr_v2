from django.db.models import Avg, Count, Q
from core_module.abstract.base_repository import BaseRepository
from talent_growth.models.talent_growth.talent_growth import PerformanceReview, PerformanceKPI, Goal


class PerformanceReviewRepository(BaseRepository):
    def __init__(self):
        super().__init__(PerformanceReview)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def get_by_period(self, period):
        return self.model.objects.filter(review_period=period)

    def get_by_status(self, status):
        return self.model.objects.filter(status=status)

    def search_reviews(self, query):
        return self.model.objects.filter(
            Q(employee__first_name__icontains=query) |
            Q(employee__last_name__icontains=query) |
            Q(employee__employee_id__icontains=query) |
            Q(review_period__icontains=query) |
            Q(department__name__icontains=query)
        )

    def get_average_rating(self, employee_id=None):
        qs = self.model.objects.filter(status='completed')
        if employee_id:
            qs = qs.filter(employee_id=employee_id)
        return qs.aggregate(avg=Avg('overall_rating'))['avg']


class PerformanceKPIRepository(BaseRepository):
    def __init__(self):
        super().__init__(PerformanceKPI)

    def get_by_review(self, review_id):
        return self.model.objects.filter(review_id=review_id)


class GoalRepository(BaseRepository):
    def __init__(self):
        super().__init__(Goal)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def get_active_goals(self):
        return self.model.objects.filter(status__in=['not_started', 'in_progress'])

    def get_overdue_goals(self):
        from datetime import date
        return self.model.objects.filter(
            due_date__lt=date.today(),
            status__in=['not_started', 'in_progress']
        )
