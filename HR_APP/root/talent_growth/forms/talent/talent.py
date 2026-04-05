from django import forms
from django.core.exceptions import ValidationError
from talent_growth.models.talent_growth.talent_growth import TalentProfile, SuccessionPlan


class TalentProfileForm(forms.ModelForm):
    class Meta:
        model = TalentProfile
        fields = [
            'employee', 'current_role', 'potential', 'performance_rating',
            'readiness', 'next_role', 'development_areas', 'key_strengths',
            'succession_plan',
        ]
        widgets = {
            'current_role': forms.TextInput(attrs={'placeholder': 'e.g. Senior Developer'}),
            'next_role': forms.TextInput(attrs={'placeholder': 'e.g. Engineering Manager'}),
            'development_areas': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Training, certifications, rotations...'}),
            'key_strengths': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_current_role(self):
        role = self.cleaned_data.get('current_role', '').strip()
        if not role:
            raise ValidationError("Current role is required.")
        if len(role) > 100:
            raise ValidationError("Current role cannot exceed 100 characters.")
        return role

    def clean_performance_rating(self):
        rating = self.cleaned_data.get('performance_rating')
        if rating is not None and (rating < 0 or rating > 5):
            raise ValidationError("Performance rating must be between 0 and 5.")
        return rating


class SuccessionPlanForm(forms.ModelForm):
    class Meta:
        model = SuccessionPlan
        fields = [
            'position', 'department', 'primary_successor', 'secondary_successors',
            'readiness_level', 'target_date', 'is_active',
        ]
        widgets = {
            'position': forms.TextInput(attrs={'placeholder': 'e.g. CTO, Sales Director'}),
            'readiness_level': forms.TextInput(attrs={'placeholder': 'e.g. Ready Now'}),
            'target_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_position(self):
        position = self.cleaned_data.get('position', '').strip()
        if not position:
            raise ValidationError("Position is required.")
        if len(position) > 100:
            raise ValidationError("Position cannot exceed 100 characters.")
        return position

    def clean_readiness_level(self):
        level = self.cleaned_data.get('readiness_level', '').strip()
        if not level:
            raise ValidationError("Readiness level is required.")
        return level
