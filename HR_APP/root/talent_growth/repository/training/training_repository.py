from django.db.models import Count, Q
from core_module.abstract.base_repository import BaseRepository
from talent_growth.models.talent_growth.talent_growth import TrainingCourse, CourseEnrollment


class TrainingCourseRepository(BaseRepository):
    def __init__(self):
        super().__init__(TrainingCourse)

    def get_active_courses(self):
        return self.model.objects.filter(is_active=True)

    def get_by_category(self, category):
        return self.model.objects.filter(category=category)

    def get_mandatory_courses(self):
        return self.model.objects.filter(is_mandatory=True, is_active=True)

    def search_courses(self, query):
        return self.model.objects.filter(
            Q(course_name__icontains=query) |
            Q(category__icontains=query) |
            Q(instructor__icontains=query) |
            Q(description__icontains=query)
        )

    def get_by_status(self, status):
        if status == 'active':
            return self.model.objects.filter(is_active=True)
        return self.model.objects.filter(is_active=False)


class CourseEnrollmentRepository(BaseRepository):
    def __init__(self):
        super().__init__(CourseEnrollment)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def get_by_course(self, course_id):
        return self.model.objects.filter(course_id=course_id)

    def get_by_status(self, status):
        return self.model.objects.filter(status=status)

    def get_completion_rate(self, course_id):
        enrollments = self.model.objects.filter(course_id=course_id)
        total = enrollments.count()
        if total == 0:
            return 0
        completed = enrollments.filter(status='completed').count()
        return round(completed / total * 100, 2)
