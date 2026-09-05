from django.db import models
from django.core.exceptions import ValidationError
from core_module.models.employee.employee import Employee, Department


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
        if self.start_time and self.end_time and self.start_time == self.end_time:
            raise ValidationError("Start time and end time cannot be identical.")


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
    date = models.DateField()
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
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

    def __str__(self):
        return f"{self.employee.full_name} - {self.date}"

    @property
    def total_hours(self):
        if self.check_in_time and self.check_out_time:
            from datetime import datetime, timedelta
            fmt = '%H:%M:%S'
            check_in = datetime.combine(self.date, self.check_in_time)
            check_out = datetime.combine(self.date, self.check_out_time)
            if check_out < check_in:
                check_out += timedelta(days=1)
            duration = check_out - check_in
            break_mins = self.shift.break_duration if self.shift else 0
            return round(duration.total_seconds() / 3600 - break_mins / 60, 2)
        return 0


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
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    document_attachment = models.FileField(upload_to='leave/documents/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, 
                                    related_name='approved_leaves')
    approved_at = models.DateTimeField(null=True, blank=True)
    denial_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee.full_name} - {self.leave_type} ({self.from_date} to {self.to_date})"

    @property
    def total_days(self):
        return (self.to_date - self.from_date).days + 1

    def clean(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValidationError("From date must be before or equal to To date.")
