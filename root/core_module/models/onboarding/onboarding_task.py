from django.db import models
from core_module.models.employee.employee import Employee


class OnboardingTask(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('not_applicable', 'N/A'),
    ]

    TASK_TYPE_CHOICES = [
        ('offer_letter', 'Offer Letter'),
        ('document_verification', 'Document Verification'),
        ('orientation', 'Orientation'),
        ('it_setup', 'IT Setup'),
        ('equipment', 'Equipment'),
        ('training', 'Training'),
        ('team_introduction', 'Team Introduction'),
        ('probation_review', 'Probation Review'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='onboarding_tasks')
    task_type = models.CharField(max_length=30, choices=TASK_TYPE_CHOICES)
    task_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='assigned_onboarding_tasks')
    due_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['employee', 'task_type']

    def __str__(self):
        return f"{self.employee.full_name} - {self.task_name}"
