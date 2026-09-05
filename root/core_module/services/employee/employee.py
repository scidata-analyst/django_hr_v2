from django.db import IntegrityError
from django.db.models import Count, Q
from django.core.exceptions import ValidationError
from core_module.abstract.base_service import BaseService
from core_module.repository.employee.employee import EmployeeRepository
from core_module.models.employee.employee import Employee, Department, Designation, Location


class EmployeeService(BaseService):
    def __init__(self):
        super().__init__(EmployeeRepository())

    def validate(self, **kwargs):
        errors = {}
        if 'personal_email' in kwargs:
            if Employee.objects.filter(personal_email=kwargs['personal_email']).exclude(
                pk=kwargs.get('pk')
            ).exists():
                errors['personal_email'] = 'Employee with this email already exists.'
        if 'employee_id' in kwargs:
            if Employee.objects.filter(employee_id=kwargs['employee_id']).exclude(
                pk=kwargs.get('pk')
            ).exists():
                errors['employee_id'] = 'Employee ID already exists.'
        return len(errors) == 0, errors

    def create_employee(self, data):
        if 'employee_id' not in data or not data['employee_id']:
            data['employee_id'] = self.repository.generate_employee_id()

        errors = {}
        fk_checks = {
            'department_id': (Department, 'Department'),
            'designation_id': (Designation, 'Designation'),
            'office_location_id': (Location, 'Location'),
            'reporting_manager_id': (Employee, 'Reporting Manager'),
        }
        for fk_field, (model, label) in fk_checks.items():
            fk_id = data.get(fk_field)
            if fk_id and not model.objects.filter(pk=fk_id).exists():
                errors[fk_field] = f'{label} with id {fk_id} does not exist.'

        if errors:
            return None, errors

        is_valid, errors = self.validate(**data)
        if not is_valid:
            return None, errors
        try:
            employee = self.repository.create(**data)
            return employee, {}
        except ValidationError as e:
            return None, e.message_dict
        except IntegrityError as e:
            return None, {'error': str(e)}

    def update_employee(self, pk, data):
        data['pk'] = pk

        errors = {}
        fk_checks = {
            'department_id': (Department, 'Department'),
            'designation_id': (Designation, 'Designation'),
            'office_location_id': (Location, 'Location'),
            'reporting_manager_id': (Employee, 'Reporting Manager'),
        }
        for fk_field, (model, label) in fk_checks.items():
            fk_id = data.get(fk_field)
            if fk_id is not None and fk_id != '' and not model.objects.filter(pk=fk_id).exists():
                errors[fk_field] = f'{label} with id {fk_id} does not exist.'

        if errors:
            return None, errors

        is_valid, errors = self.validate(**data)
        if not is_valid:
            return None, errors
        try:
            employee = self.repository.update(pk, **data)
            if employee is None:
                return None, {'error': 'Employee not found'}
            return employee, {}
        except ValidationError as e:
            return None, e.message_dict
        except IntegrityError as e:
            return None, {'error': str(e)}

    def search(self, query):
        return self.repository.search_employees(query)

    def get_by_department(self, department_id):
        return self.repository.get_by_department(department_id)

    def get_by_status(self, status):
        return self.repository.get_by_status(status)

    def get_active_employees(self):
        return self.repository.get_active_employees()

    def get_dashboard_stats(self):
        return Employee.objects.aggregate(
            total=Count('id'),
            active=Count('id', filter=Q(status='active')),
            probation=Count('id', filter=Q(status='probation')),
            resigned=Count('id', filter=Q(status='resigned')),
            terminated=Count('id', filter=Q(status='terminated')),
        )
