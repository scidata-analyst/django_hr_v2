from django.db import models
from core_module.models.employee.employee import Employee
from core_module.models.attendance.shift import Shift


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half Day'),
        ('late', 'Late'),
        ('on_leave', 'On Leave'),
        ('work_from_home', 'Work From Home'),
    ]

    WORK_LOCATION_CHOICES = [
        ('office', 'Office'),
        ('remote', 'Remote'),
        ('field', 'Field'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(db_index=True)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present', db_index=True)
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True)
    overtime_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    work_location = models.CharField(max_length=20, choices=WORK_LOCATION_CHOICES, default='office')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'employee']
        unique_together = ['employee', 'date']
        verbose_name_plural = "Attendances"
        indexes = [
            models.Index(fields=['date', 'status']),
            models.Index(fields=['employee', 'date']),
        ]

    def __str__(self):
        return f"{self.employee.full_name} - {self.date}"

    @property
    def total_hours(self):
        if self.check_in_time and self.check_out_time:
            from datetime import datetime, timedelta
            check_in = datetime.combine(self.date, self.check_in_time)
            check_out = datetime.combine(self.date, self.check_out_time)
            if check_out < check_in:
                check_out += timedelta(days=1)
            duration = check_out - check_in
            break_mins = self.shift.break_duration if self.shift else 0
            return round(duration.total_seconds() / 3600 - break_mins / 60, 2)
        return 0
