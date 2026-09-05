from django.db import models
from core_module.models.employee.employee import Employee


class ExitInterview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='exit_interviews')
    interviewer = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True,
                                    related_name='conducted_exit_interviews')
    interview_date = models.DateField()
    reason_for_leaving = models.TextField()
    feedback = models.TextField(blank=True)
    would_recommend = models.BooleanField(null=True)
    rating = models.PositiveIntegerField(null=True, help_text="1-5 rating")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-interview_date']

    def __str__(self):
        return f"Exit Interview - {self.employee.full_name} ({self.interview_date})"
