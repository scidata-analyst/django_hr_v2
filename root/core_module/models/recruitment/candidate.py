from django.db import models
from core_module.models.employee.employee import Employee
from core_module.models.recruitment.job import JobPosting


class Candidate(models.Model):
    SOURCE_CHOICES = [
        ('linkedin', 'LinkedIn'),
        ('bdjobs', 'BDJobs'),
        ('referral', 'Referral'),
        ('direct', 'Direct'),
        ('glassdoor', 'Glassdoor'),
        ('other', 'Other'),
    ]

    STAGE_CHOICES = [
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    applied_for = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='candidates')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, blank=True)
    current_stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='applied', db_index=True)
    experience_yrs = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    current_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    expected_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    notice_period = models.CharField(max_length=50, blank=True)
    resume = models.FileField(upload_to='recruitment/resumes/', null=True, blank=True)
    cover_letter = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    hired_employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='hired_as_candidate')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.applied_for.job_title}"
