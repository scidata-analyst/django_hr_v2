from django.db import models
from core_module.models.employee.department import Department


class Designation(models.Model):
    title = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    level = models.PositiveIntegerField(default=1, help_text="Hierarchy level (1=lowest)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['level', 'title']

    def __str__(self):
        return self.title
