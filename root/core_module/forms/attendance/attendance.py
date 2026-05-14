from django import forms
from django.core.exceptions import ValidationError
from core_module.models.attendance.attendance import Shift, Attendance, LeaveRequest


class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = [
            'shift_name', 'shift_code', 'start_time', 'end_time', 'break_duration',
            'grace_period', 'department', 'working_days', 'overtime_eligible', 'is_active',
        ]
        widgets = {
            'shift_name': forms.TextInput(attrs={'placeholder': 'e.g. Morning Shift'}),
            'shift_code': forms.TextInput(attrs={'placeholder': 'e.g. MORN'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_shift_name(self):
        name = self.cleaned_data.get('shift_name', '').strip()
        if not name:
            raise ValidationError("Shift name is required.")
        if len(name) > 100:
            raise ValidationError("Shift name cannot exceed 100 characters.")
        return name

    def clean_shift_code(self):
        code = self.cleaned_data.get('shift_code', '').strip()
        if not code:
            raise ValidationError("Shift code is required.")
        if len(code) > 20:
            raise ValidationError("Shift code cannot exceed 20 characters.")
        qs = Shift.objects.filter(shift_code__iexact=code)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("A shift with this code already exists.")
        return code

    def clean_break_duration(self):
        duration = self.cleaned_data.get('break_duration')
        if duration is not None and duration < 0:
            raise ValidationError("Break duration cannot be negative.")
        return duration

    def clean_grace_period(self):
        period = self.cleaned_data.get('grace_period')
        if period is not None and period < 0:
            raise ValidationError("Grace period cannot be negative.")
        return period

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time and end_time and start_time >= end_time:
            self.add_error('end_time', "End time must be after start time.")
        return cleaned_data


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = [
            'employee', 'date', 'check_in_time', 'check_out_time', 'status',
            'shift', 'overtime_hours', 'work_location', 'remarks',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'check_in_time': forms.TimeInput(attrs={'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'type': 'time'}),
            'remarks': forms.TextInput(attrs={'placeholder': 'Optional notes...'}),
        }

    def clean_overtime_hours(self):
        overtime = self.cleaned_data.get('overtime_hours')
        if overtime is not None and overtime < 0:
            raise ValidationError("Overtime hours cannot be negative.")
        return overtime

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_time')
        check_out = cleaned_data.get('check_out_time')
        if check_in and check_out and check_in >= check_out:
            self.add_error('check_out_time', "Check-out time must be after check-in time.")

        employee = cleaned_data.get('employee')
        date = cleaned_data.get('date')
        if employee and date:
            qs = Attendance.objects.filter(employee=employee, date=date)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('date', "An attendance record already exists for this employee on this date.")
        return cleaned_data


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = [
            'employee', 'leave_type', 'from_date', 'to_date', 'reason',
            'document_attachment',
        ]
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the reason for leave...'}),
        }

    def clean_reason(self):
        reason = self.cleaned_data.get('reason', '').strip()
        if not reason:
            raise ValidationError("Reason for leave is required.")
        return reason

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        if from_date and to_date and from_date > to_date:
            self.add_error('to_date', "To date must be on or after the from date.")
        return cleaned_data
