from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from main.models.main import UserProfile, DashboardWidget, Notification


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'employee', 'theme', 'notifications_enabled', 'email_notifications', 'language', 'timezone']

    def clean_language(self):
        language = self.cleaned_data.get('language', '').strip()
        if not language:
            raise ValidationError("Language is required.")
        if len(language) > 10:
            raise ValidationError("Language code cannot exceed 10 characters.")
        return language

    def clean_timezone(self):
        timezone = self.cleaned_data.get('timezone', '').strip()
        if not timezone:
            raise ValidationError("Timezone is required.")
        if len(timezone) > 50:
            raise ValidationError("Timezone cannot exceed 50 characters.")
        return timezone


class DashboardWidgetForm(forms.ModelForm):
    class Meta:
        model = DashboardWidget
        fields = ['user', 'widget_type', 'position', 'is_visible', 'config']

    def clean_widget_type(self):
        widget_type = self.cleaned_data.get('widget_type', '').strip()
        if not widget_type:
            raise ValidationError("Widget type is required.")
        if len(widget_type) > 50:
            raise ValidationError("Widget type cannot exceed 50 characters.")
        return widget_type

    def clean_config(self):
        import json
        config = self.cleaned_data.get('config')
        if config is not None and isinstance(config, str):
            try:
                return json.loads(config)
            except json.JSONDecodeError:
                raise ValidationError("Config must be valid JSON.")
        return config


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['user', 'notification_type', 'title', 'message', 'link', 'is_read']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError("Notification title is required.")
        if len(title) > 200:
            raise ValidationError("Title cannot exceed 200 characters.")
        return title

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if not message:
            raise ValidationError("Notification message is required.")
        return message

    def clean_link(self):
        link = self.cleaned_data.get('link', '').strip()
        if link and len(link) > 500:
            raise ValidationError("Link cannot exceed 500 characters.")
        return link
