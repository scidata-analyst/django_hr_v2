from django import forms
from django.core.exceptions import ValidationError
from operation.models.operation.operation import BenefitPlan, BenefitEnrollment


class BenefitPlanForm(forms.ModelForm):
    class Meta:
        model = BenefitPlan
        fields = [
            'plan_name', 'plan_type', 'coverage_details', 'cost_per_month',
            'employer_contribution', 'is_active',
        ]
        widgets = {
            'plan_name': forms.TextInput(attrs={'placeholder': 'e.g. Family Medical Insurance'}),
            'coverage_details': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Coverage inclusions and exclusions...'}),
            'cost_per_month': forms.NumberInput(attrs={'placeholder': '0'}),
            'employer_contribution': forms.NumberInput(attrs={'placeholder': '0.00'}),
        }

    def clean_plan_name(self):
        name = self.cleaned_data.get('plan_name', '').strip()
        if not name:
            raise ValidationError("Plan name is required.")
        if len(name) > 100:
            raise ValidationError("Plan name cannot exceed 100 characters.")
        return name

    def clean_coverage_details(self):
        details = self.cleaned_data.get('coverage_details', '').strip()
        if not details:
            raise ValidationError("Coverage details are required.")
        return details

    def clean_cost_per_month(self):
        cost = self.cleaned_data.get('cost_per_month')
        if cost is None or cost < 0:
            raise ValidationError("Cost per month cannot be negative.")
        return cost

    def clean_employer_contribution(self):
        contribution = self.cleaned_data.get('employer_contribution')
        if contribution is not None and contribution < 0:
            raise ValidationError("Employer contribution cannot be negative.")
        return contribution


class BenefitEnrollmentForm(forms.ModelForm):
    class Meta:
        model = BenefitEnrollment
        fields = [
            'employee', 'plan', 'coverage_start', 'coverage_end',
            'status', 'dependent_count',
        ]
        widgets = {
            'coverage_start': forms.DateInput(attrs={'type': 'date'}),
            'coverage_end': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_dependent_count(self):
        count = self.cleaned_data.get('dependent_count')
        if count is not None and count < 0:
            raise ValidationError("Dependent count cannot be negative.")
        return count

    def clean(self):
        cleaned_data = super().clean()
        coverage_start = cleaned_data.get('coverage_start')
        coverage_end = cleaned_data.get('coverage_end')
        if coverage_start and coverage_end and coverage_end < coverage_start:
            self.add_error('coverage_end', "Coverage end date must be on or after the start date.")

        employee = cleaned_data.get('employee')
        plan = cleaned_data.get('plan')
        if employee and plan:
            qs = BenefitEnrollment.objects.filter(employee=employee, plan=plan)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('plan', "This employee is already enrolled in this benefit plan.")
        return cleaned_data
