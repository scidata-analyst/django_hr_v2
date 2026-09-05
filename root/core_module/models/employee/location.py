from django.db import models


class Location(models.Model):
    LOCATION_TYPE_CHOICES = [
        ('headquarters', 'Headquarters'),
        ('branch', 'Branch Office'),
        ('remote', 'Remote'),
    ]

    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Bangladesh')
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPE_CHOICES, default='branch')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
