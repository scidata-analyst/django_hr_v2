from core_module.abstract.base_service import BaseService
from talent_growth.repository.performance.performance_repository import (
    PerformanceReviewRepository, PerformanceKPIRepository, GoalRepository
)


class PerformanceReviewService(BaseService):
    def __init__(self):
        super().__init__(PerformanceReviewRepository())

    def create_review(self, data):
        return self.repository.create(**data), {}

    def complete_review(self, review_id, overall_rating, reviewer_comments=''):
        from django.utils import timezone
        review = self.repository.update(
            review_id,
            status='completed',
            overall_rating=overall_rating,
            reviewer_comments=reviewer_comments,
            completed_at=timezone.now()
        )
        if review is None:
            return None, {'error': 'Review not found'}
        return review, {}

    def get_by_employee(self, employee_id):
        return self.repository.get_by_employee(employee_id)

    def get_average_rating(self, employee_id=None):
        return self.repository.get_average_rating(employee_id)


class PerformanceKPIService(BaseService):
    def __init__(self):
        super().__init__(PerformanceKPIRepository())

    def create_kpi(self, data):
        return self.repository.create(**data), {}

    def get_by_review(self, review_id):
        return self.repository.get_by_review(review_id)


class GoalService(BaseService):
    def __init__(self):
        super().__init__(GoalRepository())

    def create_goal(self, data):
        return self.repository.create(**data), {}

    def update_progress(self, goal_id, progress, status=None):
        data = {'progress': progress}
        if status:
            data['status'] = status
        elif progress >= 100:
            data['status'] = 'completed'
        goal = self.repository.update(goal_id, **data)
        if goal is None:
            return None, {'error': 'Goal not found'}
        return goal, {}

    def get_by_employee(self, employee_id):
        return self.repository.get_by_employee(employee_id)

    def get_overdue_goals(self):
        return self.repository.get_overdue_goals()
