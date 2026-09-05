from django.db import models
from core_module.models.employee.department import Department


class Shift(models.Model):
    WORKING_DAYS_CHOICES = [
        ('sun_thu', 'Sun–Thu'),
        ('mon_fri', 'Mon–Fri'),
        ('mon_sat', 'Mon–Sat'),
        ('rotating', 'Rotating'),
    ]

    shift_name = models.CharField(max_length=100)
    shift_code = models.CharField(max_length=20, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_duration = models.PositiveIntegerField(default=60, help_text="Break duration in minutes")
    grace_period = models.PositiveIntegerField(default=15, help_text="Grace period in minutes")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,
                                   help_text="Leave empty for all departments")
    working_days = models.CharField(max_length=20, choices=WORKING_DAYS_CHOICES, default='sun_thu')
    overtime_eligible = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['shift_name']

    def __str__(self):
        return f"{self.shift_name} ({self.shift_code})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_time and self.end_time and self.start_time == self.end_time:
            raise ValidationError("Start time and end time cannot be identical.")
