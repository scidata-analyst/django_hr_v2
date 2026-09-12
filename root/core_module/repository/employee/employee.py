from django.db.models import Q, Count
from core_module.abstract.base_repository import BaseRepository
from core_module.models.employee.employee import Employee


class EmployeeRepository(BaseRepository):
    def __init__(self):
        super().__init__(Employee)

    def get_by_employee_id(self, employee_id):
        try:
            return self.model.objects.get(employee_id=employee_id)
        except self.model.DoesNotExist:
            return None

    def get_by_department(self, department_id):
        return self.model.objects.filter(department_id=department_id)

    def get_by_status(self, status):
        return self.model.objects.filter(status=status)

    def get_active_employees(self):
        return self.model.objects.filter(status='active')

    def get_by_manager(self, manager_id):
        return self.model.objects.filter(reporting_manager_id=manager_id)

    def search_employees(self, query):
        return self.search(
            ['first_name', 'last_name', 'employee_id', 'personal_email', 'work_email', 'phone_number'],
            query
        )

    def get_by_location(self, location_id):
        return self.model.objects.filter(office_location_id=location_id)

    def get_probation_employees(self):
        return self.model.objects.filter(status='probation')

    def get_resigned_employees(self):
        return self.model.objects.filter(status='resigned')

    def generate_employee_id(self):
        last = self.model.objects.order_by('-id').first()
        if last and last.employee_id:
            try:
                # Support both EMP0001 and EMP-0001 formats
                cleaned = last.employee_id.replace('EMP-', '').replace('EMP', '')
                last_num = int(cleaned)
                return f"EMP{last_num + 1:04d}"
            except ValueError:
                pass
        # Fallback: find max numeric suffix across all IDs
        max_num = 0
        for eid in self.model.objects.values_list('employee_id', flat=True):
            try:
                cleaned = eid.replace('EMP-', '').replace('EMP', '')
                max_num = max(max_num, int(cleaned))
            except Exception:
                continue
        return f"EMP{max_num + 1:04d}" if max_num else "EMP0001"
