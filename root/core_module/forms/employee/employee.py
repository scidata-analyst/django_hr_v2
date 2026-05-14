from django import forms
from django.core.exceptions import ValidationError
from core_module.models.employee.employee import Employee, Department, Designation, Location, Document


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender', 'national_id', 'blood_group',
            'personal_email', 'work_email', 'phone_number', 'emergency_contact_name',
            'emergency_contact_phone', 'current_address', 'employee_id', 'join_date',
            'department', 'designation', 'reporting_manager', 'office_location',
            'employment_type', 'status', 'basic_salary', 'pay_frequency', 'avatar',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'join_date': forms.DateInput(attrs={'type': 'date'}),
            'current_address': forms.Textarea(attrs={'rows': 3}),
            'personal_email': forms.EmailInput(attrs={'placeholder': 'personal@email.com'}),
            'work_email': forms.EmailInput(attrs={'placeholder': 'work@company.com'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+880 1XXX XXXXXX'}),
            'emergency_contact_name': forms.TextInput(attrs={'placeholder': 'Name & Phone'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'e.g. Kabir'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'e.g. Hossain'}),
            'national_id': forms.TextInput(attrs={'placeholder': 'NID Number'}),
            'designation': forms.TextInput(attrs={'placeholder': 'e.g. Senior Developer'}),
            'basic_salary': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'employee_id': forms.TextInput(attrs={'placeholder': 'Auto-generated'}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()
        if not first_name:
            raise ValidationError("First name is required.")
        if len(first_name) > 50:
            raise ValidationError("First name cannot exceed 50 characters.")
        if not first_name.replace(' ', '').isalpha():
            raise ValidationError("First name can only contain letters and spaces.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').strip()
        if not last_name:
            raise ValidationError("Last name is required.")
        if len(last_name) > 50:
            raise ValidationError("Last name cannot exceed 50 characters.")
        if not last_name.replace(' ', '').isalpha():
            raise ValidationError("Last name can only contain letters and spaces.")
        return last_name

    def clean_personal_email(self):
        email = self.cleaned_data.get('personal_email', '').strip()
        if not email:
            raise ValidationError("Personal email is required.")
        return email

    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id', '').strip()
        if not employee_id:
            raise ValidationError("Employee ID is required.")
        if len(employee_id) > 20:
            raise ValidationError("Employee ID cannot exceed 20 characters.")
        qs = Employee.objects.filter(employee_id=employee_id)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("This Employee ID already exists.")
        return employee_id

    def clean_basic_salary(self):
        salary = self.cleaned_data.get('basic_salary')
        if salary is not None and salary < 0:
            raise ValidationError("Basic salary cannot be negative.")
        return salary

    def clean_join_date(self):
        join_date = self.cleaned_data.get('join_date')
        if join_date and join_date > __import__('datetime').date.today():
            raise ValidationError("Join date cannot be in the future.")
        return join_date

    def clean(self):
        cleaned_data = super().clean()
        work_email = cleaned_data.get('work_email')
        personal_email = cleaned_data.get('personal_email')
        if work_email and personal_email and work_email == personal_email:
            self.add_error('work_email', "Work email must be different from personal email.")
        return cleaned_data


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError("Department name is required.")
        if len(name) > 100:
            raise ValidationError("Department name cannot exceed 100 characters.")
        qs = Department.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("A department with this name already exists.")
        return name


class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['title', 'department', 'level']

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError("Designation title is required.")
        if len(title) > 100:
            raise ValidationError("Title cannot exceed 100 characters.")
        qs = Designation.objects.filter(title__iexact=title)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("A designation with this title already exists.")
        return title

    def clean_level(self):
        level = self.cleaned_data.get('level')
        if level is not None and level < 1:
            raise ValidationError("Level must be at least 1.")
        return level


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'city', 'country', 'location_type', 'is_active']

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError("Location name is required.")
        if len(name) > 100:
            raise ValidationError("Location name cannot exceed 100 characters.")
        qs = Location.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("A location with this name already exists.")
        return name

    def clean_city(self):
        city = self.cleaned_data.get('city', '').strip()
        if not city:
            raise ValidationError("City is required.")
        return city

    def clean_country(self):
        country = self.cleaned_data.get('country', '').strip()
        if not country:
            raise ValidationError("Country is required.")
        return country


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['employee', 'document_type', 'title', 'file', 'status', 'expiry_date', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError("Document title is required.")
        if len(title) > 100:
            raise ValidationError("Title cannot exceed 100 characters.")
        return title

    def clean(self):
        cleaned_data = super().clean()
        expiry_date = cleaned_data.get('expiry_date')
        if expiry_date and expiry_date < __import__('datetime').date.today():
            self.add_error('expiry_date', "Expiry date cannot be in the past.")
        return cleaned_data
