from django import forms
from django.core.exceptions import ValidationError
from core_module.models.payroll.payroll import SalaryStructure, Payslip, Loan, LoanRepayment, Bonus


class SalaryStructureForm(forms.ModelForm):
    class Meta:
        model = SalaryStructure
        fields = [
            'structure_name', 'grade_level', 'basic_salary', 'house_rent_percent',
            'transport_allowance', 'medical_allowance', 'food_allowance', 'other_allowance',
            'income_tax_percent', 'provident_fund_percent', 'insurance_premium', 'other_deductions',
            'is_active',
        ]
        widgets = {
            'structure_name': forms.TextInput(attrs={'placeholder': 'e.g. Senior Engineer Grade A'}),
            'grade_level': forms.TextInput(attrs={'placeholder': 'e.g. Grade 5'}),
            'basic_salary': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'house_rent_percent': forms.NumberInput(attrs={'placeholder': '20'}),
            'transport_allowance': forms.NumberInput(attrs={'placeholder': '100'}),
            'medical_allowance': forms.NumberInput(attrs={'placeholder': '80'}),
            'food_allowance': forms.NumberInput(attrs={'placeholder': '50'}),
            'other_allowance': forms.NumberInput(attrs={'placeholder': '0'}),
            'income_tax_percent': forms.NumberInput(attrs={'placeholder': '10'}),
            'provident_fund_percent': forms.NumberInput(attrs={'placeholder': '8'}),
            'insurance_premium': forms.NumberInput(attrs={'placeholder': '30'}),
            'other_deductions': forms.NumberInput(attrs={'placeholder': '0'}),
        }

    def clean_structure_name(self):
        name = self.cleaned_data.get('structure_name', '').strip()
        if not name:
            raise ValidationError("Structure name is required.")
        if len(name) > 100:
            raise ValidationError("Structure name cannot exceed 100 characters.")
        qs = SalaryStructure.objects.filter(structure_name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("A salary structure with this name already exists.")
        return name

    def clean_basic_salary(self):
        salary = self.cleaned_data.get('basic_salary')
        if salary is None or salary <= 0:
            raise ValidationError("Basic salary must be greater than zero.")
        return salary

    def clean_house_rent_percent(self):
        percent = self.cleaned_data.get('house_rent_percent')
        if percent is not None and (percent < 0 or percent > 100):
            raise ValidationError("House rent percentage must be between 0 and 100.")
        return percent

    def clean_income_tax_percent(self):
        percent = self.cleaned_data.get('income_tax_percent')
        if percent is not None and (percent < 0 or percent > 100):
            raise ValidationError("Income tax percentage must be between 0 and 100.")
        return percent

    def clean_provident_fund_percent(self):
        percent = self.cleaned_data.get('provident_fund_percent')
        if percent is not None and (percent < 0 or percent > 100):
            raise ValidationError("Provident fund percentage must be between 0 and 100.")
        return percent


class PayslipForm(forms.ModelForm):
    class Meta:
        model = Payslip
        fields = [
            'employee', 'salary_structure', 'pay_period', 'pay_date', 'basic_salary',
            'house_rent', 'transport_allowance', 'medical_allowance', 'food_allowance',
            'other_allowance', 'overtime_amount', 'bonus_amount', 'income_tax',
            'provident_fund', 'insurance_deduction', 'other_deductions', 'loan_emi',
            'absent_deduction', 'late_deduction',
        ]
        widgets = {
            'pay_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_pay_period(self):
        period = self.cleaned_data.get('pay_period', '').strip()
        if not period:
            raise ValidationError("Pay period is required.")
        if len(period) > 20:
            raise ValidationError("Pay period cannot exceed 20 characters.")
        return period

    def clean_basic_salary(self):
        salary = self.cleaned_data.get('basic_salary')
        if salary is None or salary < 0:
            raise ValidationError("Basic salary cannot be negative.")
        return salary

    def clean(self):
        cleaned_data = super().clean()
        employee = cleaned_data.get('employee')
        pay_period = cleaned_data.get('pay_period')
        if employee and pay_period:
            qs = Payslip.objects.filter(employee=employee, pay_period=pay_period)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('pay_period', "A payslip already exists for this employee in this period.")
        return cleaned_data


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = [
            'employee', 'loan_type', 'loan_amount', 'disbursement_date', 'repayment_period',
            'interest_rate', 'status', 'purpose_notes',
        ]
        widgets = {
            'disbursement_date': forms.DateInput(attrs={'type': 'date'}),
            'loan_amount': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'repayment_period': forms.NumberInput(attrs={'placeholder': '12'}),
            'interest_rate': forms.NumberInput(attrs={'placeholder': '0'}),
            'purpose_notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Reason for loan...'}),
        }

    def clean_loan_amount(self):
        amount = self.cleaned_data.get('loan_amount')
        if amount is None or amount <= 0:
            raise ValidationError("Loan amount must be greater than zero.")
        return amount

    def clean_repayment_period(self):
        period = self.cleaned_data.get('repayment_period')
        if period is None or period <= 0:
            raise ValidationError("Repayment period must be at least 1 month.")
        return period

    def clean_interest_rate(self):
        rate = self.cleaned_data.get('interest_rate')
        if rate is not None and rate < 0:
            raise ValidationError("Interest rate cannot be negative.")
        return rate


class BonusForm(forms.ModelForm):
    class Meta:
        model = Bonus
        fields = [
            'employee', 'is_all_employees', 'bonus_type', 'amount', 'pay_month',
            'taxable', 'status', 'remarks',
        ]
        widgets = {
            'pay_month': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'remarks': forms.TextInput(attrs={'placeholder': 'Reason for bonus...'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None or amount <= 0:
            raise ValidationError("Bonus amount must be greater than zero.")
        return amount

    def clean(self):
        cleaned_data = super().clean()
        is_all = cleaned_data.get('is_all_employees')
        employee = cleaned_data.get('employee')
        if not is_all and not employee:
            self.add_error('employee', "Either select an employee or mark as 'All Employees'.")
        return cleaned_data
