from django.db import models
from core_module.models.employee.employee import Employee


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
