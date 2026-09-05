from django.db import models
from django.core.exceptions import ValidationError
from core_module.models.employee.employee import Employee


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
