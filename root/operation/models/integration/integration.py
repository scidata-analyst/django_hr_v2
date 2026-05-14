from django.db import models
from core_module.models.employee.employee import Employee


class Integration(models.Model):
    INTEGRATION_TYPE_CHOICES = [
        ('payroll', 'Payroll System'),
        ('calendar', 'Calendar'),
        ('storage', 'Cloud Storage'),
        ('communication', 'Communication'),
        ('analytics', 'Analytics'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('error', 'Error'),
    ]

    name = models.CharField(max_length=100)
    integration_type = models.CharField(max_length=20, choices=INTEGRATION_TYPE_CHOICES)
    api_key = models.CharField(max_length=500, blank=True)
    api_secret = models.CharField(max_length=500, blank=True)
    webhook_url = models.URLField(blank=True)
    is_enabled = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    last_sync = models.DateTimeField(null=True, blank=True)
    settings = models.TextField(blank=True, help_text="JSON settings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.status})"
