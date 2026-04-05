from django import forms
from django.core.exceptions import ValidationError
from operation.models.operation.operation import Integration


class IntegrationForm(forms.ModelForm):
    class Meta:
        model = Integration
        fields = [
            'name', 'integration_type', 'api_key', 'api_secret', 'webhook_url',
            'is_enabled', 'status', 'last_sync', 'settings',
        ]
        widgets = {
            'api_key': forms.PasswordInput(attrs={'placeholder': 'API Key'}),
            'api_secret': forms.PasswordInput(attrs={'placeholder': 'API Secret'}),
            'webhook_url': forms.URLInput(attrs={'placeholder': 'https://yourhrms.com/webhook/...'}),
            'settings': forms.Textarea(attrs={'rows': 3, 'placeholder': 'JSON settings'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError("Integration name is required.")
        if len(name) > 100:
            raise ValidationError("Integration name cannot exceed 100 characters.")
        return name

    def clean_webhook_url(self):
        url = self.cleaned_data.get('webhook_url', '').strip()
        if url and not url.startswith(('http://', 'https://')):
            raise ValidationError("Please enter a valid URL starting with http:// or https://")
        return url

    def clean_settings(self):
        import json
        settings = self.cleaned_data.get('settings', '').strip()
        if settings:
            try:
                json.loads(settings)
            except json.JSONDecodeError:
                raise ValidationError("Settings must be valid JSON.")
        return settings
