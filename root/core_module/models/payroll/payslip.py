from django.db import models
from core_module.models.employee.employee import Employee
from core_module.models.payroll.structure import SalaryStructure


class Payslip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payslips')
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.SET_NULL, null=True, blank=True)
    pay_period = models.CharField(max_length=20, help_text="e.g., January 2026", db_index=True)
    pay_date = models.DateField(db_index=True)
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    house_rent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    food_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overtime_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    income_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    provident_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    insurance_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    loan_emi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    absent_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    late_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pdf_file = models.FileField(upload_to='payslips/', null=True, blank=True)
    is_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pay_date']
        unique_together = ['employee', 'pay_period']
        indexes = [
            models.Index(fields=['pay_period', 'pay_date']),
            models.Index(fields=['employee', 'pay_period']),
        ]

    def __str__(self):
        return f"{self.employee.full_name} - {self.pay_period}"

    @property
    def gross_salary(self):
        return self.basic_salary + self.house_rent + self.transport_allowance + \
               self.medical_allowance + self.food_allowance + self.other_allowance + \
               self.overtime_amount + self.bonus_amount

    @property
    def total_deductions(self):
        return self.income_tax + self.provident_fund + self.insurance_deduction + \
               self.other_deductions + self.loan_emi + self.absent_deduction + self.late_deduction

    @property
    def net_pay(self):
        return self.gross_salary - self.total_deductions
