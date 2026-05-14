from django import forms
from django.core.exceptions import ValidationError
from talent_growth.models.talent_growth.talent_growth import TrainingCourse, CourseEnrollment


class TrainingCourseForm(forms.ModelForm):
    class Meta:
        model = TrainingCourse
        fields = [
            'course_name', 'category', 'description', 'duration_hours',
            'instructor', 'is_mandatory', 'is_active',
        ]
        widgets = {
            'course_name': forms.TextInput(attrs={'placeholder': 'e.g. Leadership Excellence Program'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Course overview and objectives...'}),
            'instructor': forms.TextInput(attrs={'placeholder': 'Internal or external trainer'}),
            'duration_hours': forms.NumberInput(attrs={'placeholder': '8'}),
        }

    def clean_course_name(self):
        name = self.cleaned_data.get('course_name', '').strip()
        if not name:
            raise ValidationError("Course name is required.")
        if len(name) > 200:
            raise ValidationError("Course name cannot exceed 200 characters.")
        return name

    def clean_duration_hours(self):
        duration = self.cleaned_data.get('duration_hours')
        if duration is not None and duration < 1:
            raise ValidationError("Duration must be at least 1 hour.")
        return duration


class CourseEnrollmentForm(forms.ModelForm):
    class Meta:
        model = CourseEnrollment
        fields = [
            'employee', 'course', 'completion_date',
            'status', 'score', 'certificate', 'feedback',
        ]
        widgets = {
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
            'score': forms.NumberInput(attrs={'placeholder': '0-100'}),
            'feedback': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score is not None and (score < 0 or score > 100):
            raise ValidationError("Score must be between 0 and 100.")
        return score

    def clean(self):
        cleaned_data = super().clean()
        employee = cleaned_data.get('employee')
        course = cleaned_data.get('course')
        if employee and course:
            qs = CourseEnrollment.objects.filter(employee=employee, course=course)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('course', "This employee is already enrolled in this course.")
        return cleaned_data
