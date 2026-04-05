from django import forms
from django.core.exceptions import ValidationError
from talent_growth.models.talent_growth.talent_growth import PerformanceReview, PerformanceKPI, Goal


class PerformanceReviewForm(forms.ModelForm):
    class Meta:
        model = PerformanceReview
        fields = [
            'employee', 'department', 'review_period', 'start_date', 'end_date',
            'overall_rating', 'status', 'reviewer', 'employee_comments', 'reviewer_comments',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'employee_comments': forms.Textarea(attrs={'rows': 3}),
            'reviewer_comments': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_review_period(self):
        period = self.cleaned_data.get('review_period', '').strip()
        if not period:
            raise ValidationError("Review period is required.")
        if len(period) > 20:
            raise ValidationError("Review period cannot exceed 20 characters.")
        return period

    def clean_overall_rating(self):
        rating = self.cleaned_data.get('overall_rating')
        if rating is not None and (rating < 0 or rating > 5):
            raise ValidationError("Overall rating must be between 0 and 5.")
        return rating

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and start_date > end_date:
            self.add_error('end_date', "End date must be on or after the start date.")
        return cleaned_data


class PerformanceKPIForm(forms.ModelForm):
    class Meta:
        model = PerformanceKPI
        fields = ['review', 'metric', 'target', 'score', 'weight', 'notes']
        widgets = {
            'target': forms.TextInput(attrs={'placeholder': 'e.g. 95% uptime / $100K revenue'}),
            'score': forms.NumberInput(attrs={'placeholder': '0-100'}),
            'weight': forms.NumberInput(attrs={'placeholder': '20'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_metric(self):
        metric = self.cleaned_data.get('metric', '').strip()
        if not metric:
            raise ValidationError("Metric name is required.")
        if len(metric) > 200:
            raise ValidationError("Metric name cannot exceed 200 characters.")
        return metric

    def clean_target(self):
        target = self.cleaned_data.get('target', '').strip()
        if not target:
            raise ValidationError("Target is required.")
        return target

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score is not None and (score < 0 or score > 100):
            raise ValidationError("Score must be between 0 and 100.")
        return score

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight is not None and weight <= 0:
            raise ValidationError("Weight must be greater than zero.")
        return weight


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = [
            'employee', 'title', 'description', 'start_date', 'due_date',
            'status', 'progress', 'parent_goal',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Deliver Project Alpha on time'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Detailed description of the goal...'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'progress': forms.NumberInput(attrs={'min': 0, 'max': 100, 'placeholder': '0'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError("Goal title is required.")
        if len(title) > 200:
            raise ValidationError("Title cannot exceed 200 characters.")
        return title

    def clean_progress(self):
        progress = self.cleaned_data.get('progress')
        if progress is not None and (progress < 0 or progress > 100):
            raise ValidationError("Progress must be between 0 and 100.")
        return progress

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        due_date = cleaned_data.get('due_date')
        if start_date and due_date and start_date > due_date:
            self.add_error('due_date', "Due date must be on or after the start date.")

        parent_goal = cleaned_data.get('parent_goal')
        if self.instance.pk and parent_goal and parent_goal.pk == self.instance.pk:
            self.add_error('parent_goal', "A goal cannot be its own parent.")
        return cleaned_data
