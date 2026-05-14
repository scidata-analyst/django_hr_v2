from core_module.abstract.base_service import BaseService
from talent_growth.repository.training.training_repository import (
    TrainingCourseRepository, CourseEnrollmentRepository
)


class TrainingCourseService(BaseService):
    def __init__(self):
        super().__init__(TrainingCourseRepository())

    def get_active_courses(self):
        return self.repository.get_active_courses()

    def get_mandatory_courses(self):
        return self.repository.get_mandatory_courses()


class CourseEnrollmentService(BaseService):
    def __init__(self):
        super().__init__(CourseEnrollmentRepository())

    def enroll_employee(self, data):
        return self.repository.create(**data), {}

    def complete_enrollment(self, enrollment_id, score=None, feedback=''):
        from datetime import date
        data = {'status': 'completed', 'completion_date': date.today()}
        if score is not None:
            data['score'] = score
        if feedback:
            data['feedback'] = feedback
        enrollment = self.repository.update(enrollment_id, **data)
        if enrollment is None:
            return None, {'error': 'Enrollment not found'}
        return enrollment, {}

    def get_by_employee(self, employee_id):
        return self.repository.get_by_employee(employee_id)

    def bulk_enroll(self, course_id, employee_ids):
        results = {'enrolled': 0, 'skipped': 0}
        for emp_id in employee_ids:
            try:
                self.repository.create(employee_id=emp_id, course_id=course_id)
                results['enrolled'] += 1
            except Exception:
                results['skipped'] += 1
        return results
