from django import forms
from django.core.exceptions import ValidationError
from operation.models.operation.operation import SafetyIncident


class SafetyIncidentForm(forms.ModelForm):
    class Meta:
        model = SafetyIncident
        fields = [
            'reported_by', 'incident_date', 'location', 'severity', 'description',
            'injuries', 'witnesses', 'corrective_action', 'status', 'assigned_to',
        ]
        widgets = {
            'incident_date': forms.DateInput(attrs={'type': 'date'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Warehouse Floor 2'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe what happened in detail...'}),
            'injuries': forms.Textarea(attrs={'rows': 3}),
            'witnesses': forms.TextInput(attrs={'placeholder': 'Witness names...'}),
            'corrective_action': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Immediate actions and preventive measures...'}),
        }

    def clean_location(self):
        location = self.cleaned_data.get('location', '').strip()
        if not location:
            raise ValidationError("Incident location is required.")
        if len(location) > 200:
            raise ValidationError("Location cannot exceed 200 characters.")
        return location

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if not description:
            raise ValidationError("Incident description is required.")
        return description

    def clean_incident_date(self):
        incident_date = self.cleaned_data.get('incident_date')
        if incident_date and incident_date > __import__('datetime').date.today():
            raise ValidationError("Incident date cannot be in the future.")
        return incident_date
