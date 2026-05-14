from django import forms
from django.core.exceptions import ValidationError
from core_module.models.onboarding.onboarding import OnboardingTask, OffboardingTask, ExitInterview


class OnboardingTaskForm(forms.ModelForm):
    class Meta:
        model = OnboardingTask
        fields = [
            'employee', 'task_type', 'task_name', 'description', 'assigned_to',
            'due_date', 'status', 'notes',
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Onboarding notes...'}),
        }

    def clean_task_name(self):
        name = self.cleaned_data.get('task_name', '').strip()
        if not name:
            raise ValidationError("Task name is required.")
        if len(name) > 100:
            raise ValidationError("Task name cannot exceed 100 characters.")
        return name

    def clean(self):
        cleaned_data = super().clean()
        due_date = cleaned_data.get('due_date')
        if due_date and due_date < __import__('datetime').date.today():
            self.add_error('due_date', "Due date cannot be in the past.")
        return cleaned_data


class OffboardingTaskForm(forms.ModelForm):
    class Meta:
        model = OffboardingTask
        fields = [
            'employee', 'task_type', 'task_name', 'description', 'assigned_to',
            'due_date', 'status', 'notes',
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Offboarding notes...'}),
        }

    def clean_task_name(self):
        name = self.cleaned_data.get('task_name', '').strip()
        if not name:
            raise ValidationError("Task name is required.")
        if len(name) > 100:
            raise ValidationError("Task name cannot exceed 100 characters.")
        return name

    def clean(self):
        cleaned_data = super().clean()
        due_date = cleaned_data.get('due_date')
        if due_date and due_date < __import__('datetime').date.today():
            self.add_error('due_date', "Due date cannot be in the past.")
        return cleaned_data


class ExitInterviewForm(forms.ModelForm):
    class Meta:
        model = ExitInterview
        fields = [
            'employee', 'interviewer', 'interview_date', 'reason_for_leaving',
            'feedback', 'would_recommend', 'rating',
        ]
        widgets = {
            'interview_date': forms.DateInput(attrs={'type': 'date'}),
            'reason_for_leaving': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Key feedback from exit interview...'}),
            'feedback': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_reason_for_leaving(self):
        reason = self.cleaned_data.get('reason_for_leaving', '').strip()
        if not reason:
            raise ValidationError("Reason for leaving is required.")
        return reason

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None and (rating < 1 or rating > 5):
            raise ValidationError("Rating must be between 1 and 5.")
        return rating

    def clean_interview_date(self):
        interview_date = self.cleaned_data.get('interview_date')
        if interview_date and interview_date > __import__('datetime').date.today():
            raise ValidationError("Interview date cannot be in the future.")
        return interview_date
