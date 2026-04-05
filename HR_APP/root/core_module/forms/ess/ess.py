from django import forms
from django.core.exceptions import ValidationError
from core_module.models.ess.ess import ExpenseClaim, Announcement


class ExpenseClaimForm(forms.ModelForm):
    class Meta:
        model = ExpenseClaim
        fields = [
            'employee', 'category', 'amount', 'expense_date', 'description', 'receipt',
        ]
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'expense_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None or amount <= 0:
            raise ValidationError("Expense amount must be greater than zero.")
        return amount

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if not description:
            raise ValidationError("Description is required.")
        return description

    def clean_expense_date(self):
        expense_date = self.cleaned_data.get('expense_date')
        if expense_date and expense_date > __import__('datetime').date.today():
            raise ValidationError("Expense date cannot be in the future.")
        return expense_date


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [
            'title', 'content', 'priority', 'is_pinned', 'published_by',
            'expires_at', 'is_active',
        ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError("Announcement title is required.")
        if len(title) > 200:
            raise ValidationError("Title cannot exceed 200 characters.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise ValidationError("Announcement content is required.")
        return content

    def clean(self):
        cleaned_data = super().clean()
        expires_at = cleaned_data.get('expires_at')
        if expires_at and expires_at < __import__('datetime').datetime.now(tz=__import__('django').utils.timezone.get_current_timezone()):
            self.add_error('expires_at', "Expiry date cannot be in the past.")
        return cleaned_data
