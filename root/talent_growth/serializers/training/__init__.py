from talent_growth.models.training.training import TrainingCourse, CourseEnrollment


class TrainingCourseSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'course_name': instance.course_name,
            'category': instance.category,
            'description': instance.description,
            'duration_hours': instance.duration_hours,
            'instructor': instance.instructor,
            'is_mandatory': instance.is_mandatory,
            'is_active': instance.is_active,
        }

    @staticmethod
    def serialize_list(qs):
        return [TrainingCourseSerializer.serialize(obj) for obj in qs]


class CourseEnrollmentSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'employee': instance.employee.full_name if instance.employee else None,
            'course': instance.course.course_name if instance.course else None,
            'enrollment_date': str(instance.enrollment_date),
            'completion_date': str(instance.completion_date) if instance.completion_date else None,
            'status': instance.status,
            'score': float(instance.score) if instance.score else None,
            'feedback': instance.feedback,
        }

    @staticmethod
    def serialize_list(qs):
        return [CourseEnrollmentSerializer.serialize(obj) for obj in qs]
