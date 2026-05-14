from django.db import models
from django.contrib.auth.models import User
from core_module.models.employee.employee import Employee


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    employee = models.OneToOneField(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='user_profile')
    theme = models.CharField(max_length=20, default='light')
    notifications_enabled = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    language = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=50, default='Asia/Dhaka')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.username}"


class DashboardWidget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_widgets')
    widget_type = models.CharField(max_length=50)
    position = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    config = models.TextField(default='{}', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f"{self.user.username} - {self.widget_type}"


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('info', 'Info'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default='info')
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"
