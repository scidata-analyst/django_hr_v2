from talent_growth.models.talent_growth.talent_growth import (
    PerformanceReview, PerformanceKPI, Goal, TrainingCourse, CourseEnrollment,
    TalentProfile, SuccessionPlan, EngagementSurvey, SurveyResponse, SurveyQuestion, Recognition
)


class PerformanceReviewSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'employee_id': obj.employee_id,
            'employee_name': obj.employee.full_name,
            'department_id': obj.department_id,
            'department_name': obj.department.name if obj.department else None,
            'review_period': obj.review_period,
            'start_date': obj.start_date.isoformat(),
            'end_date': obj.end_date.isoformat(),
            'overall_rating': str(obj.overall_rating) if obj.overall_rating else None,
            'status': obj.status,
            'status_display': obj.get_status_display(),
            'reviewer_id': obj.reviewer_id,
            'reviewer_name': obj.reviewer.full_name if obj.reviewer else None,
            'employee_comments': obj.employee_comments,
            'reviewer_comments': obj.reviewer_comments,
            'completed_at': obj.completed_at.isoformat() if obj.completed_at else None,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(qs):
        return [PerformanceReviewSerializer.serialize(o) for o in qs]


class PerformanceKPISerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'review_id': obj.review_id,
            'metric': obj.metric,
            'target': obj.target,
            'score': str(obj.score) if obj.score else None,
            'weight': str(obj.weight),
            'notes': obj.notes,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(qs):
        return [PerformanceKPISerializer.serialize(o) for o in qs]


class GoalSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'employee_id': obj.employee_id,
            'employee_name': obj.employee.full_name,
            'title': obj.title,
            'description': obj.description,
            'start_date': obj.start_date.isoformat(),
            'due_date': obj.due_date.isoformat(),
            'status': obj.status,
            'status_display': obj.get_status_display(),
            'progress': obj.progress,
            'parent_goal_id': obj.parent_goal_id,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(qs):
        return [GoalSerializer.serialize(o) for o in qs]


class TrainingCourseSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'course_name': obj.course_name,
            'category': obj.category,
            'category_display': obj.get_category_display(),
            'description': obj.description,
            'duration_hours': obj.duration_hours,
            'instructor': obj.instructor,
            'is_mandatory': obj.is_mandatory,
            'is_active': obj.is_active,
            'enrollment_count': obj.enrollments.count(),
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(qs):
        return [TrainingCourseSerializer.serialize(o) for o in qs]


class CourseEnrollmentSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'employee_id': obj.employee_id,
            'employee_name': obj.employee.full_name,
            'course_id': obj.course_id,
            'course_name': obj.course.course_name,
            'enrollment_date': obj.enrollment_date.isoformat(),
            'completion_date': obj.completion_date.isoformat() if obj.completion_date else None,
            'status': obj.status,
            'status_display': obj.get_status_display(),
            'score': str(obj.score) if obj.score else None,
            'certificate': obj.certificate.url if obj.certificate else None,
            'feedback': obj.feedback,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(qs):
        return [CourseEnrollmentSerializer.serialize(o) for o in qs]


class TalentProfileSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'employee_id': obj.employee_id,
            'employee_name': obj.employee.full_name,
            'current_role': obj.current_role,
            'potential': obj.potential,
            'potential_display': obj.get_potential_display(),
            'performance_rating': str(obj.performance_rating) if obj.performance_rating else None,
            'readiness': obj.readiness,
            'readiness_display': obj.get_readiness_display(),
            'next_role': obj.next_role,
            'development_areas': obj.development_areas,
            'key_strengths': obj.key_strengths,
            'succession_plan': obj.succession_plan,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(qs):
        return [TalentProfileSerializer.serialize(o) for o in qs]


class SuccessionPlanSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'position': obj.position,
            'department_id': obj.department_id,
            'department_name': obj.department.name if obj.department else None,
            'primary_successor_id': obj.primary_successor_id,
            'primary_successor_name': obj.primary_successor.full_name if obj.primary_successor else None,
            'secondary_successors': [
                {'id': s.id, 'name': s.full_name} for s in obj.secondary_successors.all()
            ],
            'readiness_level': obj.readiness_level,
            'target_date': obj.target_date.isoformat() if obj.target_date else None,
            'is_active': obj.is_active,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(qs):
        return [SuccessionPlanSerializer.serialize(o) for o in qs]


class EngagementSurveySerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'title': obj.title,
            'description': obj.description,
            'start_date': obj.start_date.isoformat(),
            'end_date': obj.end_date.isoformat(),
            'is_anonymous': obj.is_anonymous,
            'is_active': obj.is_active,
            'response_count': obj.responses.count(),
            'question_count': obj.questions.count(),
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(qs):
        return [EngagementSurveySerializer.serialize(o) for o in qs]


class RecognitionSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'employee_id': obj.employee_id,
            'employee_name': obj.employee.full_name,
            'recognized_by_id': obj.recognized_by_id,
            'recognized_by_name': obj.recognized_by.full_name if obj.recognized_by else None,
            'recognition_type': obj.recognition_type,
            'recognition_type_display': obj.get_recognition_type_display(),
            'reason': obj.reason,
            'points': obj.points,
            'given_at': obj.given_at.isoformat(),
        }

    @staticmethod
    def serialize_list(qs):
        return [RecognitionSerializer.serialize(o) for o in qs]
