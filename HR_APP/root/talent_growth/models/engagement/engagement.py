from django.db import models
from core_module.models.employee.employee import Employee


class EngagementSurvey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_anonymous = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title


class SurveyQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('rating', 'Rating Scale'),
        ('text', 'Text Response'),
        ('multiple_choice', 'Multiple Choice'),
    ]

    survey = models.ForeignKey(EngagementSurvey, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    options = models.TextField(blank=True, help_text="Comma-separated options for multiple choice")
    order = models.PositiveIntegerField(default=0)
    is_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['survey', 'order']

    def __str__(self):
        return f"{self.survey.title} - Q{self.order}"


class SurveyResponse(models.Model):
    survey = models.ForeignKey(EngagementSurvey, on_delete=models.CASCADE, related_name='responses')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='survey_responses',
                                null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    overall_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.survey.title} - Response"


class Recognition(models.Model):
    RECOGNITION_TYPE_CHOICES = [
        ('kudos', 'Kudos'),
        ('peer_award', 'Peer Award'),
        ('innovation', 'Innovation Award'),
        ('team_player', 'Team Player'),
        ('leader', 'Leader Award'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='recognitions')
    recognized_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True,
                                      related_name='given_recognitions')
    recognition_type = models.CharField(max_length=20, choices=RECOGNITION_TYPE_CHOICES)
    reason = models.TextField()
    points = models.PositiveIntegerField(default=0)
    given_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-given_at']

    def __str__(self):
        return f"{self.recognized_by} recognized {self.employee} - {self.recognition_type}"
