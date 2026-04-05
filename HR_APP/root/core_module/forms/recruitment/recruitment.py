from django import forms
from django.core.exceptions import ValidationError
from core_module.models.recruitment.recruitment import JobPosting, Candidate, Interview


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            'job_title', 'department', 'job_type', 'location', 'salary_range_min',
            'salary_range_max', 'vacancies', 'application_deadline', 'experience_required',
            'education_level', 'job_description', 'skills_required', 'publish_on', 'status',
        ]
        widgets = {
            'job_title': forms.TextInput(attrs={'placeholder': 'e.g. Senior Backend Developer'}),
            'salary_range_min': forms.NumberInput(attrs={'placeholder': 'Min salary'}),
            'salary_range_max': forms.NumberInput(attrs={'placeholder': 'Max salary'}),
            'vacancies': forms.NumberInput(attrs={'placeholder': '1'}),
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
            'job_description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe responsibilities and requirements...'}),
            'skills_required': forms.TextInput(attrs={'placeholder': 'e.g. React, Node.js, PostgreSQL (comma separated)'}),
        }

    def clean_job_title(self):
        title = self.cleaned_data.get('job_title', '').strip()
        if not title:
            raise ValidationError("Job title is required.")
        if len(title) > 200:
            raise ValidationError("Job title cannot exceed 200 characters.")
        return title

    def clean_job_description(self):
        description = self.cleaned_data.get('job_description', '').strip()
        if not description:
            raise ValidationError("Job description is required.")
        return description

    def clean_vacancies(self):
        vacancies = self.cleaned_data.get('vacancies')
        if vacancies is not None and vacancies < 1:
            raise ValidationError("Vacancies must be at least 1.")
        return vacancies

    def clean(self):
        cleaned_data = super().clean()
        salary_min = cleaned_data.get('salary_range_min')
        salary_max = cleaned_data.get('salary_range_max')
        if salary_min and salary_max and salary_min > salary_max:
            self.add_error('salary_range_max', "Maximum salary cannot be less than minimum salary.")
        return cleaned_data


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            'full_name', 'email', 'phone', 'applied_for', 'source', 'current_stage',
            'experience_yrs', 'current_salary', 'expected_salary', 'notice_period',
            'resume', 'cover_letter', 'linkedin_url', 'portfolio_url',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Candidate name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'candidate@email.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '+880...'}),
            'experience_yrs': forms.NumberInput(attrs={'placeholder': 'Years of experience'}),
            'current_salary': forms.NumberInput(attrs={'placeholder': '0'}),
            'expected_salary': forms.NumberInput(attrs={'placeholder': '0'}),
            'cover_letter': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Recruiter notes...'}),
        }

    def clean_full_name(self):
        name = self.cleaned_data.get('full_name', '').strip()
        if not name:
            raise ValidationError("Candidate full name is required.")
        if len(name) > 100:
            raise ValidationError("Full name cannot exceed 100 characters.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise ValidationError("Candidate email is required.")
        return email

    def clean_experience_yrs(self):
        exp = self.cleaned_data.get('experience_yrs')
        if exp is not None and exp < 0:
            raise ValidationError("Years of experience cannot be negative.")
        return exp

    def clean_expected_salary(self):
        salary = self.cleaned_data.get('expected_salary')
        if salary is not None and salary < 0:
            raise ValidationError("Expected salary cannot be negative.")
        return salary

    def clean_linkedin_url(self):
        url = self.cleaned_data.get('linkedin_url', '').strip()
        if url and not url.startswith(('http://', 'https://')):
            raise ValidationError("Please enter a valid URL starting with http:// or https://")
        return url

    def clean_portfolio_url(self):
        url = self.cleaned_data.get('portfolio_url', '').strip()
        if url and not url.startswith(('http://', 'https://')):
            raise ValidationError("Please enter a valid URL starting with http:// or https://")
        return url


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = [
            'candidate', 'interview_type', 'scheduled_at', 'duration_mins', 'interviewer',
            'location', 'meeting_link', 'result', 'feedback', 'rating',
        ]
        widgets = {
            'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'duration_mins': forms.NumberInput(attrs={'placeholder': '60'}),
            'location': forms.TextInput(attrs={'placeholder': 'Zoom link or room number'}),
            'meeting_link': forms.URLInput(attrs={'placeholder': 'https://zoom.us/...'}),
            'feedback': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Interview instructions or focus areas...'}),
            'rating': forms.NumberInput(attrs={'placeholder': '1-5'}),
        }

    def clean_duration_mins(self):
        duration = self.cleaned_data.get('duration_mins')
        if duration is not None and duration < 1:
            raise ValidationError("Duration must be at least 1 minute.")
        return duration

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None and (rating < 1 or rating > 5):
            raise ValidationError("Rating must be between 1 and 5.")
        return rating

    def clean_meeting_link(self):
        url = self.cleaned_data.get('meeting_link', '').strip()
        if url and not url.startswith(('http://', 'https://')):
            raise ValidationError("Please enter a valid URL starting with http:// or https://")
        return url
