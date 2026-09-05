from django.db.models import Count
from core_module.abstract.base_repository import BaseRepository
from core_module.models.employee.employee import Department


class DepartmentRepository(BaseRepository):
    def __init__(self):
        super().__init__(Department)

    def get_with_employee_count(self):
        return self.model.objects.annotate(employee_count=Count('employee_set'))

    def get_all(self):
        return self.model.objects.annotate(employee_count=Count('employee_set'))

    def search_departments(self, query):
        return self.search(['name', 'description'], query).annotate(employee_count=Count('employee_set'))
