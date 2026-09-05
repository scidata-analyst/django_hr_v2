from django.test import TestCase

from core_module.models.employee.employee import (
    Department, Location, Designation, Employee, Document,
)


class DepartmentModelTest(TestCase):
    def test_str_returns_name(self):
        dept = Department.objects.create(name='Engineering')
        self.assertEqual(str(dept), 'Engineering')


class EmployeeModelTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(name='Engineering')
        self.desig = Designation.objects.create(title='Developer')
        self.emp = Employee.objects.create(
            first_name='John',
            last_name='Doe',
            employee_id='EMP-0001',
            join_date='2026-01-01',
            personal_email='john@example.com',
            department=self.dept,
            designation=self.desig,
            basic_salary=50000,
        )

    def test_full_name(self):
        self.assertEqual(self.emp.full_name, 'John Doe')

    def test_str(self):
        self.assertEqual(str(self.emp), 'John Doe (EMP-0001)')

    def test_tenure(self):
        tenure = self.emp.tenure
        self.assertIn('years', tenure)
