from django.db import models
from django.core.exceptions import ValidationError
from core_module.models.employee.employee import Employee


class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('annual', 'Annual'),
        ('sick', 'Sick'),
        ('casual', 'Casual'),
        ('maternity', 'Maternity'),
        ('paternity', 'Paternity'),
        ('emergency', 'Emergency'),
        ('unpaid', 'Unpaid'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    from_date = models.DateField(db_index=True)
    to_date = models.DateField(db_index=True)
    reason = models.TextField()
    document_attachment = models.FileField(upload_to='leave/documents/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='approved_leaves')
    approved_at = models.DateTimeField(null=True, blank=True)
    denial_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['employee', 'status']),
            models.Index(fields=['status', 'from_date']),
        ]

    def __str__(self):
        return f"{self.employee.full_name} - {self.leave_type} ({self.from_date} to {self.to_date})"

    @property
    def total_days(self):
        return (self.to_date - self.from_date).days + 1

    def clean(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValidationError("From date must be before or equal to To date.")
