from django.db import models
from core_module.models.employee.employee import Employee


class PolicyDocument(models.Model):
    CATEGORY_CHOICES = [
        ('governance', 'Governance'),
        ('operations', 'Operations'),
        ('hr', 'HR'),
        ('legal', 'Legal'),
        ('safety', 'Safety'),
        ('it', 'IT'),
    ]

    policy_name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    version = models.CharField(max_length=20, default='1.0')
    description = models.TextField(blank=True)
    document_file = models.FileField(upload_to='policies/documents/')
    effective_date = models.DateField()
    review_date = models.DateField(null=True, blank=True)
    is_mandatory = models.BooleanField(default=False)
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='created_policies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-effective_date']

    def __str__(self):
        return f"{self.policy_name} v{self.version}"


class PolicyAcknowledgement(models.Model):
    policy = models.ForeignKey(PolicyDocument, on_delete=models.CASCADE, related_name='acknowledgements')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='policy_acknowledgements')
    acknowledged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['policy', 'employee']
        ordering = ['-acknowledged_at']

    def __str__(self):
        return f"{self.employee.full_name} acknowledged {self.policy.policy_name}"


class ComplianceChecklist(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('not_applicable', 'N/A'),
    ]

    checklist_name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=PolicyDocument.CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_checklists')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.checklist_name
