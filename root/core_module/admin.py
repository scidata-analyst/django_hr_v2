from django.contrib import admin

from core_module.models.employee.employee import (
    Department, Location, Designation, Employee, Document,
)
from core_module.models.attendance.attendance import (
    Shift, Attendance, LeaveRequest,
)
from core_module.models.onboarding.onboarding import (
    OnboardingTask, OffboardingTask, ExitInterview,
)
from core_module.models.payroll.payroll import (
    SalaryStructure, Payslip, Loan, LoanRepayment, Bonus,
)
from core_module.models.recruitment.recruitment import (
    JobPosting, Candidate, Interview,
)
from core_module.models.ess.ess import (
    ExpenseClaim, Announcement,
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'location_type', 'is_active')
    list_filter = ('location_type', 'is_active', 'country')
    search_fields = ('name', 'city')


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'level')
    list_filter = ('department',)
    search_fields = ('title',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'first_name', 'last_name', 'department', 'designation', 'status', 'join_date')
    list_filter = ('status', 'employment_type', 'department', 'office_location')
    search_fields = ('employee_id', 'first_name', 'last_name', 'personal_email', 'work_email')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'document_type', 'title', 'status', 'uploaded_at')
    list_filter = ('document_type', 'status')
    search_fields = ('title',)


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('shift_name', 'shift_code', 'start_time', 'end_time', 'is_active')
    list_filter = ('is_active', 'working_days')
    search_fields = ('shift_name', 'shift_code')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status', 'shift', 'work_location')
    list_filter = ('status', 'work_location', 'date')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__employee_id')
    date_hierarchy = 'date'


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'from_date', 'to_date', 'status')
    list_filter = ('leave_type', 'status')
    search_fields = ('employee__first_name', 'employee__last_name')


@admin.register(OnboardingTask)
class OnboardingTaskAdmin(admin.ModelAdmin):
    list_display = ('employee', 'task_type', 'task_name', 'status', 'due_date')
    list_filter = ('task_type', 'status')


@admin.register(OffboardingTask)
class OffboardingTaskAdmin(admin.ModelAdmin):
    list_display = ('employee', 'task_type', 'task_name', 'status', 'due_date')
    list_filter = ('task_type', 'status')


@admin.register(ExitInterview)
class ExitInterviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'interview_date', 'would_recommend', 'rating')
    list_filter = ('would_recommend', 'rating')


@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = ('structure_name', 'grade_level', 'basic_salary', 'is_active')
    list_filter = ('is_active', 'grade_level')
    search_fields = ('structure_name',)


@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ('employee', 'pay_period', 'pay_date', 'basic_salary', 'is_generated')
    list_filter = ('pay_period', 'is_generated')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__employee_id')
    date_hierarchy = 'pay_date'


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('employee', 'loan_type', 'loan_amount', 'status', 'disbursement_date')
    list_filter = ('loan_type', 'status')


@admin.register(LoanRepayment)
class LoanRepaymentAdmin(admin.ModelAdmin):
    list_display = ('loan', 'repayment_date', 'amount', 'remaining_balance')
    date_hierarchy = 'repayment_date'


@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    list_display = ('employee', 'bonus_type', 'amount', 'pay_month', 'status')
    list_filter = ('bonus_type', 'status')


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'department', 'job_type', 'status', 'application_deadline')
    list_filter = ('status', 'job_type', 'department')
    search_fields = ('job_title',)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'applied_for', 'current_stage', 'created_at')
    list_filter = ('current_stage', 'source')
    search_fields = ('full_name', 'email', 'phone')


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'interview_type', 'scheduled_at', 'result')
    list_filter = ('interview_type', 'result')
    date_hierarchy = 'scheduled_at'


@admin.register(ExpenseClaim)
class ExpenseClaimAdmin(admin.ModelAdmin):
    list_display = ('employee', 'category', 'amount', 'status', 'expense_date')
    list_filter = ('status', 'category')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'is_pinned', 'published_at', 'is_active')
    list_filter = ('priority', 'is_pinned', 'is_active')
