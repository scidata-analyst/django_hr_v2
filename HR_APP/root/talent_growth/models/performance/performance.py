from django.db import models
from core_module.models.employee.employee import Employee, Department


class PerformanceReview(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance_reviews')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    review_period = models.CharField(max_length=20, help_text="e.g., Q4 2025")
    start_date = models.DateField()
    end_date = models.DateField()
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True,
                                         help_text="Rating out of 5")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    reviewer = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='conducted_reviews')
    employee_comments = models.TextField(blank=True)
    reviewer_comments = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-review_period']
        verbose_name = "Performance Review"
        verbose_name_plural = "Performance Reviews"

    def __str__(self):
        return f"{self.employee.full_name} - {self.review_period}"


class PerformanceKPI(models.Model):
    review = models.ForeignKey(PerformanceReview, on_delete=models.CASCADE, related_name='kpis')
    metric = models.CharField(max_length=200)
    target = models.TextField()
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                               help_text="Score percentage")
    weight = models.DecimalField(max_digits=3, decimal_places=2, default=1.0,
                                 help_text="Weight for calculation")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.review.employee.full_name} - {self.metric}"


class Goal(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    progress = models.PositiveIntegerField(default=0, help_text="Progress percentage (0-100)")
    parent_goal = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='sub_goals')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee.full_name} - {self.title}"
