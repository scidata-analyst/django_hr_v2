from django.db import models
from core_module.models.employee.employee import Employee


class TrainingCourse(models.Model):
    CATEGORY_CHOICES = [
        ('management', 'Management'),
        ('compliance', 'Compliance'),
        ('technical', 'Technical'),
        ('soft_skills', 'Soft Skills'),
        ('safety', 'Safety'),
        ('onboarding', 'Onboarding'),
        ('leadership', 'Leadership'),
    ]

    course_name = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    duration_hours = models.PositiveIntegerField(default=1)
    instructor = models.CharField(max_length=100, blank=True)
    is_mandatory = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['course_name']

    def __str__(self):
        return self.course_name


class CourseEnrollment(models.Model):
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='course_enrollments')
    course = models.ForeignKey(TrainingCourse, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                               help_text="Completion score percentage")
    certificate = models.FileField(upload_to='training/certificates/', null=True, blank=True)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-enrollment_date']
        unique_together = ['employee', 'course']

    def __str__(self):
        return f"{self.employee.full_name} - {self.course.course_name}"
