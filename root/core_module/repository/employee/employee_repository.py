from django.db.models import Q, Count
from core_module.abstract.base_repository import BaseRepository
from core_module.models.employee.employee import Department, Location, Designation, Employee, Document


class DepartmentRepository(BaseRepository):
    def __init__(self):
        super().__init__(Department)

    def get_with_employee_count(self):
        return self.model.objects.annotate(employee_count=Count('employee_set'))

    def search_departments(self, query):
        return self.search(['name', 'description'], query)


class LocationRepository(BaseRepository):
    def __init__(self):
        super().__init__(Location)

    def get_active(self):
        return self.model.objects.filter(is_active=True)

    def get_by_type(self, location_type):
        return self.model.objects.filter(location_type=location_type)


class DesignationRepository(BaseRepository):
    def __init__(self):
        super().__init__(Designation)

    def get_by_department(self, department_id):
        return self.model.objects.filter(department_id=department_id)

    def get_by_level(self, level):
        return self.model.objects.filter(level=level)


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
                last_num = int(last.employee_id.replace('EMP-', ''))
                return f"EMP-{last_num + 1:04d}"
            except ValueError:
                pass
        return "EMP-0001"


class DocumentRepository(BaseRepository):
    def __init__(self):
        super().__init__(Document)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def get_by_type(self, document_type):
        return self.model.objects.filter(document_type=document_type)

    def get_pending_documents(self):
        return self.model.objects.filter(status='pending')

    def get_expired_documents(self):
        from datetime import date
        return self.model.objects.filter(expiry_date__lt=date.today(), status='verified')
