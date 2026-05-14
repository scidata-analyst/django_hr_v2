from django import forms
from django.core.exceptions import ValidationError
from talent_growth.models.talent_growth.talent_growth import Recognition, EngagementSurvey, SurveyQuestion, SurveyResponse


class RecognitionForm(forms.ModelForm):
    class Meta:
        model = Recognition
        fields = [
            'employee', 'recognized_by', 'recognition_type', 'reason', 'points',
        ]
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write a meaningful appreciation message...'}),
            'points': forms.NumberInput(attrs={'placeholder': '100'}),
        }

    def clean_reason(self):
        reason = self.cleaned_data.get('reason', '').strip()
        if not reason:
            raise ValidationError("Reason for recognition is required.")
        return reason

    def clean_points(self):
        points = self.cleaned_data.get('points')
        if points is not None and points < 0:
            raise ValidationError("Points cannot be negative.")
        return points


class EngagementSurveyForm(forms.ModelForm):
    class Meta:
        model = EngagementSurvey
        fields = [
            'title', 'description', 'start_date', 'end_date', 'is_anonymous', 'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Q1 2026 Employee Engagement Survey'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError("Survey title is required.")
        if len(title) > 200:
            raise ValidationError("Title cannot exceed 200 characters.")
        return title

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and start_date > end_date:
            self.add_error('end_date', "End date must be on or after the start date.")
        return cleaned_data


class SurveyQuestionForm(forms.ModelForm):
    class Meta:
        model = SurveyQuestion
        fields = ['survey', 'question_text', 'question_type', 'options', 'order', 'is_required']
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'e.g. How satisfied are you with work-life balance? (1-5)'}),
            'options': forms.TextInput(attrs={'placeholder': 'Comma-separated options'}),
        }

    def clean_question_text(self):
        text = self.cleaned_data.get('question_text', '').strip()
        if not text:
            raise ValidationError("Question text is required.")
        return text


class SurveyResponseForm(forms.ModelForm):
    class Meta:
        model = SurveyResponse
        fields = ['survey', 'employee', 'overall_score']
        widgets = {
            'overall_score': forms.NumberInput(attrs={'placeholder': '0-100'}),
        }

    def clean_overall_score(self):
        score = self.cleaned_data.get('overall_score')
        if score is not None and (score < 0 or score > 100):
            raise ValidationError("Overall score must be between 0 and 100.")
        return score
