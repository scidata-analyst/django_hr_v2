from django.db import models
from core_module.models.employee.employee import Employee


class BenefitPlan(models.Model):
    PLAN_TYPE_CHOICES = [
        ('medical', 'Medical'),
        ('dental', 'Dental'),
        ('vision', 'Vision'),
        ('life_insurance', 'Life Insurance'),
        ('disability', 'Disability'),
        ('wellness', 'Wellness'),
        ('retirement', 'Retirement'),
    ]

    plan_name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES)
    coverage_details = models.TextField()
    cost_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    employer_contribution = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['plan_name']

    def __str__(self):
        return f"{self.plan_name} ({self.plan_type})"


class BenefitEnrollment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='benefit_enrollments')
    plan = models.ForeignKey(BenefitPlan, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    coverage_start = models.DateField()
    coverage_end = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    dependent_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-enrollment_date']
        unique_together = ['employee', 'plan']

    def __str__(self):
        return f"{self.employee.full_name} - {self.plan.plan_name}"


class SafetyIncident(models.Model):
    SEVERITY_CHOICES = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
        ('critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    reported_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reported_incidents')
    incident_date = models.DateField()
    location = models.CharField(max_length=200)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    description = models.TextField()
    injuries = models.TextField(blank=True)
    witnesses = models.TextField(blank=True)
    corrective_action = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_incidents')
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-incident_date']

    def __str__(self):
        return f"Incident #{self.id} - {self.incident_date}"
