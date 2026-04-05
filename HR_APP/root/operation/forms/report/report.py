from django import forms
from django.core.exceptions import ValidationError
from operation.models.operation.operation import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_name', 'report_type', 'description', 'parameters', 'created_by']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'parameters': forms.Textarea(attrs={'rows': 3, 'placeholder': 'JSON of report parameters'}),
        }

    def clean_report_name(self):
        name = self.cleaned_data.get('report_name', '').strip()
        if not name:
            raise ValidationError("Report name is required.")
        if len(name) > 200:
            raise ValidationError("Report name cannot exceed 200 characters.")
        return name

    def clean_parameters(self):
        import json
        parameters = self.cleaned_data.get('parameters', '').strip()
        if parameters:
            try:
                json.loads(parameters)
            except json.JSONDecodeError:
                raise ValidationError("Parameters must be valid JSON.")
        return parameters
