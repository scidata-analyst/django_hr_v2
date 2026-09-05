from django.test import TestCase

from core_module.services.employee.employee import EmployeeService
from core_module.models.employee.employee import Department


class EmployeeServiceTest(TestCase):
    def test_create_employee_generates_id(self):
        service = EmployeeService()
        dept = Department.objects.create(name='HR')
        employee, errors = service.create_employee({
            'first_name': 'Jane',
            'last_name': 'Doe',
            'personal_email': 'jane@example.com',
            'join_date': '2026-02-01',
            'department_id': dept.id,
            'basic_salary': 60000,
        })
        self.assertIsNone(errors or None) or self.assertEqual(errors, {})
        self.assertIsNotNone(employee)
        self.assertTrue(employee.employee_id.startswith('EMP-'))

    def test_dashboard_stats_returns_all_keys(self):
        service = EmployeeService()
        stats = service.get_dashboard_stats()
        for key in ('total', 'active', 'probation', 'resigned', 'terminated'):
            self.assertIn(key, stats)
