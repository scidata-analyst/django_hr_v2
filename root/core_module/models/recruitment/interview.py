from django.db import models
from core_module.models.employee.employee import Employee
from core_module.models.recruitment.candidate import Candidate


class Interview(models.Model):
    INTERVIEW_TYPE_CHOICES = [
        ('phone', 'Phone'),
        ('video', 'Video'),
        ('technical', 'Technical'),
        ('hr', 'HR'),
        ('final', 'Final'),
    ]

    RESULT_CHOICES = [
        ('pending', 'Pending'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
    ]

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='interviews')
    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPE_CHOICES)
    scheduled_at = models.DateTimeField()
    duration_mins = models.PositiveIntegerField(default=60)
    interviewer = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='conducted_interviews')
    location = models.CharField(max_length=100, blank=True)
    meeting_link = models.URLField(blank=True)
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, default='pending')
    feedback = models.TextField(blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True, help_text="1-5 rating")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_at']

    def __str__(self):
        return f"{self.candidate.full_name} - {self.interview_type} ({self.scheduled_at.date()})"
