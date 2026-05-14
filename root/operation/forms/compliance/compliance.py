from django import forms
from django.core.exceptions import ValidationError
from operation.models.operation.operation import PolicyDocument, PolicyAcknowledgement, ComplianceChecklist


class PolicyDocumentForm(forms.ModelForm):
    class Meta:
        model = PolicyDocument
        fields = [
            'policy_name', 'category', 'version', 'description', 'document_file',
            'effective_date', 'review_date', 'is_mandatory', 'created_by',
        ]
        widgets = {
            'policy_name': forms.TextInput(attrs={'placeholder': 'e.g. Remote Work Policy'}),
            'version': forms.TextInput(attrs={'placeholder': 'e.g. v1.0'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Brief summary of the policy...'}),
            'effective_date': forms.DateInput(attrs={'type': 'date'}),
            'review_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_policy_name(self):
        name = self.cleaned_data.get('policy_name', '').strip()
        if not name:
            raise ValidationError("Policy name is required.")
        if len(name) > 200:
            raise ValidationError("Policy name cannot exceed 200 characters.")
        return name

    def clean_version(self):
        version = self.cleaned_data.get('version', '').strip()
        if not version:
            raise ValidationError("Version is required.")
        if len(version) > 20:
            raise ValidationError("Version cannot exceed 20 characters.")
        return version

    def clean_effective_date(self):
        effective_date = self.cleaned_data.get('effective_date')
        if not effective_date:
            raise ValidationError("Effective date is required.")
        return effective_date

    def clean(self):
        cleaned_data = super().clean()
        effective_date = cleaned_data.get('effective_date')
        review_date = cleaned_data.get('review_date')
        if effective_date and review_date and review_date < effective_date:
            self.add_error('review_date', "Review date must be on or after the effective date.")
        return cleaned_data


class ComplianceChecklistForm(forms.ModelForm):
    class Meta:
        model = ComplianceChecklist
        fields = [
            'checklist_name', 'category', 'description', 'due_date',
            'assigned_to', 'status', 'notes',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_checklist_name(self):
        name = self.cleaned_data.get('checklist_name', '').strip()
        if not name:
            raise ValidationError("Checklist name is required.")
        if len(name) > 200:
            raise ValidationError("Checklist name cannot exceed 200 characters.")
        return name
