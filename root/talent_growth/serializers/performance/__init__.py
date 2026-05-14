from talent_growth.models.performance.performance import PerformanceReview, PerformanceKPI, Goal


class PerformanceReviewSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'employee': instance.employee.full_name if instance.employee else None,
            'department': instance.department.name if instance.department else None,
            'review_period': instance.review_period,
            'start_date': str(instance.start_date),
            'end_date': str(instance.end_date),
            'overall_rating': float(instance.overall_rating) if instance.overall_rating else None,
            'status': instance.status,
            'reviewer': instance.reviewer.full_name if instance.reviewer else None,
            'employee_comments': instance.employee_comments,
            'reviewer_comments': instance.reviewer_comments,
        }

    @staticmethod
    def serialize_list(qs):
        return [PerformanceReviewSerializer.serialize(obj) for obj in qs]


class PerformanceKPISerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'review_id': instance.review_id,
            'metric': instance.metric,
            'target': instance.target,
            'score': float(instance.score) if instance.score else None,
            'weight': float(instance.weight) if instance.weight else None,
            'notes': instance.notes,
        }

    @staticmethod
    def serialize_list(qs):
        return [PerformanceKPISerializer.serialize(obj) for obj in qs]


class GoalSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'employee': instance.employee.full_name if instance.employee else None,
            'title': instance.title,
            'description': instance.description,
            'start_date': str(instance.start_date),
            'due_date': str(instance.due_date),
            'status': instance.status,
            'progress': instance.progress,
            'parent_goal_id': instance.parent_goal_id,
        }

    @staticmethod
    def serialize_list(qs):
        return [GoalSerializer.serialize(obj) for obj in qs]
