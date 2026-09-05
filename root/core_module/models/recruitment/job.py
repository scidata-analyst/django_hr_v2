from django.db import models
from django.core.exceptions import ValidationError
from core_module.models.employee.department import Department
from core_module.models.employee.location import Location
from core_module.models.employee.employee import Employee


class JobPosting(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]

    EXPERIENCE_CHOICES = [
        ('fresher', 'Fresher'),
        ('1_2_years', '1-2 years'),
        ('3_5_years', '3-5 years'),
        ('5_10_years', '5-10 years'),
        ('10_plus', '10+ years'),
    ]

    EDUCATION_CHOICES = [
        ('any', 'Any'),
        ('hsc', 'HSC'),
        ('bachelor', "Bachelor's"),
        ('master', "Master's"),
        ('phd', 'PhD'),
    ]

    PUBLISH_CHOICES = [
        ('linkedin_bdjobs', 'LinkedIn + BDJobs'),
        ('linkedin', 'LinkedIn only'),
        ('internal', 'Internal only'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('draft', 'Draft'),
        ('on_hold', 'On Hold'),
        ('closed', 'Closed'),
    ]

    job_title = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    salary_range_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_range_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    vacancies = models.PositiveIntegerField(default=1)
    application_deadline = models.DateField(null=True, blank=True)
    experience_required = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, blank=True)
    education_level = models.CharField(max_length=20, choices=EDUCATION_CHOICES, blank=True)
    job_description = models.TextField()
    skills_required = models.TextField(blank=True, help_text="Comma-separated skills")
    publish_on = models.CharField(max_length=30, choices=PUBLISH_CHOICES, default='internal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='created_jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Job Posting"
        verbose_name_plural = "Job Postings"

    def __str__(self):
        return f"{self.job_title} ({self.status})"

    def clean(self):
        if self.salary_range_min and self.salary_range_max and self.salary_range_min > self.salary_range_max:
            raise ValidationError("Minimum salary cannot be greater than maximum salary.")
