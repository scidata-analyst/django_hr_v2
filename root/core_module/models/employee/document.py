from django.db import models
from core_module.models.employee.employee import Employee


class Document(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('offer_letter', 'Offer Letter'),
        ('nid', 'NID Copy'),
        ('academic_certificate', 'Academic Certificate'),
        ('tax_document', 'Tax Document'),
        ('medical_certificate', 'Medical Certificate'),
        ('experience_certificate', 'Experience Certificate'),
        ('contract', 'Contract'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('verified', 'Verified'),
        ('pending', 'Pending'),
        ('missing', 'Missing'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='employees/documents/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    expiry_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.employee.full_name} - {self.title}"
