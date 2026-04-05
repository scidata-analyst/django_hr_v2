from django import forms
from django.core.exceptions import ValidationError
from operation.models.global_.global_ import Office


class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
        fields = [
            'name', 'country', 'city', 'office_type', 'full_address',
            'local_currency', 'timezone', 'hr_contact', 'tax_law',
            'labor_law', 'capacity', 'status',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. London Office'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'full_address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Complete office address...'}),
            'tax_law': forms.TextInput(attrs={'placeholder': 'e.g. Bangladesh Income Tax Ordinance'}),
            'labor_law': forms.TextInput(attrs={'placeholder': 'e.g. Bangladesh Labor Act 2006'}),
            'capacity': forms.NumberInput(attrs={'placeholder': 'Max headcount'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError("Office name is required.")
        if len(name) > 100:
            raise ValidationError("Office name cannot exceed 100 characters.")
        return name

    def clean_city(self):
        city = self.cleaned_data.get('city', '').strip()
        if not city:
            raise ValidationError("City is required.")
        if len(city) > 100:
            raise ValidationError("City cannot exceed 100 characters.")
        return city

    def clean_country(self):
        country = self.cleaned_data.get('country', '').strip()
        if not country:
            raise ValidationError("Country is required.")
        if len(country) > 100:
            raise ValidationError("Country cannot exceed 100 characters.")
        return country

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity is not None and capacity < 0:
            raise ValidationError("Capacity cannot be negative.")
        return capacity
