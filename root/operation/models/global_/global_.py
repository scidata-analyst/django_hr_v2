from django.db import models
from core_module.models.employee.employee import Employee


class Office(models.Model):
    OFFICE_TYPE_CHOICES = [
        ('headquarters', 'Headquarters'),
        ('regional', 'Regional Office'),
        ('branch', 'Branch Office'),
        ('remote_hub', 'Remote Hub'),
    ]

    CURRENCY_CHOICES = [
        ('BDT', 'BDT'),
        ('USD', 'USD'),
        ('GBP', 'GBP'),
        ('AED', 'AED'),
        ('INR', 'INR'),
    ]

    TIMEZONE_CHOICES = [
        ('Asia/Dhaka', 'Asia/Dhaka (UTC+6)'),
        ('Europe/London', 'Europe/London (UTC+0/+1)'),
        ('Asia/Dubai', 'Asia/Dubai (UTC+4)'),
        ('America/New_York', 'America/New_York (UTC-5/-4)'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('planned', 'Planned'),
    ]

    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    office_type = models.CharField(max_length=20, choices=OFFICE_TYPE_CHOICES)
    full_address = models.TextField(blank=True)
    local_currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='BDT')
    timezone = models.CharField(max_length=50, choices=TIMEZONE_CHOICES, default='Asia/Dhaka')
    hr_contact = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='hr_contact_offices')
    tax_law = models.CharField(max_length=200, blank=True)
    labor_law = models.CharField(max_length=200, blank=True)
    capacity = models.PositiveIntegerField(default=0, help_text="Max headcount")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.city}, {self.country})"
