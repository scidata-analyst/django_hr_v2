from django.db import models
from core_module.models.employee.employee import Employee


class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('attendance', 'Attendance'),
        ('payroll', 'Payroll'),
        ('headcount', 'Headcount'),
        ('turnover', 'Turnover'),
        ('performance', 'Performance'),
        ('custom', 'Custom'),
    ]

    report_name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    parameters = models.TextField(blank=True, help_text="JSON of report parameters")
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='created_reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.report_name
