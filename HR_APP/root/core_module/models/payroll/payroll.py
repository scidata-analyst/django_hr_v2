from django.db import models
from django.core.exceptions import ValidationError
from core_module.models.employee.employee import Employee


class SalaryStructure(models.Model):
    structure_name = models.CharField(max_length=100, unique=True)
    grade_level = models.CharField(max_length=20, blank=True)
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    house_rent_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    transport_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    food_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    income_tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    provident_fund_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    insurance_premium = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['structure_name']

    def __str__(self):
        return self.structure_name

    @property
    def gross_salary(self):
        house_rent = (self.basic_salary * self.house_rent_percent) / 100
        return self.basic_salary + house_rent + self.transport_allowance + \
               self.medical_allowance + self.food_allowance + self.other_allowance

    @property
    def total_deductions(self):
        house_rent = (self.basic_salary * self.house_rent_percent) / 100
        gross = self.basic_salary + house_rent + self.transport_allowance + \
                self.medical_allowance + self.food_allowance + self.other_allowance
        tax = (gross * self.income_tax_percent) / 100
        pf = (self.basic_salary * self.provident_fund_percent) / 100
        return tax + pf + self.insurance_premium + self.other_deductions

    @property
    def net_salary(self):
        return self.gross_salary - self.total_deductions


class Payslip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payslips')
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.SET_NULL, null=True, blank=True)
    pay_period = models.CharField(max_length=20, help_text="e.g., January 2026")
    pay_date = models.DateField()
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


class Loan(models.Model):
    LOAN_TYPE_CHOICES = [
        ('personal', 'Personal'),
        ('medical_advance', 'Medical Advance'),
        ('salary_advance', 'Salary Advance'),
        ('education', 'Education'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('pending', 'Pending Approval'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='loans')
    loan_type = models.CharField(max_length=30, choices=LOAN_TYPE_CHOICES)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    disbursement_date = models.DateField(null=True, blank=True)
    repayment_period = models.PositiveIntegerField(help_text="Repayment period in months")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='approved_loans')
    purpose_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee.full_name} - {self.loan_type} ({self.loan_amount})"

    @property
    def monthly_emi(self):
        if self.repayment_period > 0:
            principal = float(self.loan_amount)
            rate = float(self.interest_rate) / 100 / 12
            months = self.repayment_period
            if rate > 0:
                emi = principal * rate * (1 + rate)**months / ((1 + rate)**months - 1)
            else:
                emi = principal / months
            return round(emi, 2)
        return 0

    @property
    def total_interest(self):
        return (self.monthly_emi * self.repayment_period) - float(self.loan_amount)


class LoanRepayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayments')
    repayment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    principal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_balance = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-repayment_date']

    def __str__(self):
        return f"{self.loan} - {self.repayment_date} ({self.amount})"


class Bonus(models.Model):
    BONUS_TYPE_CHOICES = [
        ('performance', 'Performance'),
        ('festival', 'Festival'),
        ('referral', 'Referral'),
        ('retention', 'Retention'),
        ('commission', 'Commission'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='bonuses', null=True, blank=True)
    is_all_employees = models.BooleanField(default=False, help_text="Apply to all employees")
    bonus_type = models.CharField(max_length=30, choices=BONUS_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    pay_month = models.DateField(help_text="Month to be paid")
    taxable = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='approved_bonuses')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pay_month']

    def __str__(self):
        emp_name = self.employee.full_name if self.employee else "All Employees"
        return f"{emp_name} - {self.bonus_type} ({self.amount})"

    def clean(self):
        if not self.is_all_employees and not self.employee:
            raise ValidationError("Either select an employee or mark as 'All Employees'.")
