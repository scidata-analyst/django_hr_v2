from django.db import models
from core_module.models.employee.employee import Employee, Department


class TalentProfile(models.Model):
    POTENTIAL_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    READINESS_CHOICES = [
        ('ready_now', 'Ready Now'),
        ('1_year', '1 Year'),
        ('2_years', '2 Years'),
        ('3_plus_years', '3+ Years'),
        ('not_ready', 'Not Ready'),
    ]

    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='talent_profile')
    current_role = models.CharField(max_length=100)
    potential = models.CharField(max_length=10, choices=POTENTIAL_CHOICES)
    performance_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True,
                                             help_text="Current performance rating")
    readiness = models.CharField(max_length=20, choices=READINESS_CHOICES)
    next_role = models.CharField(max_length=100, blank=True)
    development_areas = models.TextField(blank=True)
    key_strengths = models.TextField(blank=True)
    succession_plan = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-potential', '-performance_rating']

    def __str__(self):
        return f"{self.employee.full_name} - {self.potential} Potential"


class SuccessionPlan(models.Model):
    position = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    primary_successor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True,
                                          related_name='primary_succession')
    secondary_successors = models.ManyToManyField(Employee, related_name='secondary_successions',
                                                   blank=True)
    readiness_level = models.CharField(max_length=20)
    target_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f"Succession for {self.position}"
