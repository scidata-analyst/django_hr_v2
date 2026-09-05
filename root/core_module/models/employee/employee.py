from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Departments"
        ordering = ['name']

    def __str__(self):
        return self.name


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


class Employee(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('intern', 'Intern'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('probation', 'Probation'),
        ('resigned', 'Resigned'),
        ('terminated', 'Terminated'),
    ]

    PAY_FREQUENCY_CHOICES = [
        ('monthly', 'Monthly'),
        ('bi_weekly', 'Bi-weekly'),
        ('weekly', 'Weekly'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    national_id = models.CharField(max_length=50, blank=True, verbose_name="National ID/Passport")
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    
    personal_email = models.EmailField()
    work_email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    current_address = models.TextField(blank=True)
    
    employee_id = models.CharField(max_length=20, unique=True)
    join_date = models.DateField(db_index=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True)
    reporting_manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='direct_reports')
    office_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='full_time')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='probation', db_index=True)
    
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    pay_frequency = models.CharField(max_length=20, choices=PAY_FREQUENCY_CHOICES, default='monthly')
    
    avatar = models.ImageField(upload_to='employees/avatars/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee')
    
    resignation_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'join_date']),
            models.Index(fields=['department', 'status']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def tenure(self):
        from datetime import date
        if self.resignation_date:
            end = self.resignation_date
        else:
            end = date.today()
        years = end.year - self.join_date.year
        months = end.month - self.join_date.month
        if months < 0:
            years -= 1
            months += 12
        return f"{years} years, {months} months"


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
