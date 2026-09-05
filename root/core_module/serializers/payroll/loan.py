from core_module.models.payroll.loan import Loan, LoanRepayment


class LoanSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'employee_id': obj.employee_id,
            'employee_name': obj.employee.full_name,
            'loan_type': obj.loan_type,
            'loan_type_display': obj.get_loan_type_display(),
            'loan_amount': str(obj.loan_amount),
            'disbursement_date': obj.disbursement_date.isoformat() if obj.disbursement_date else None,
            'repayment_period': obj.repayment_period,
            'monthly_emi': str(obj.monthly_emi),
            'total_interest': str(obj.total_interest),
            'interest_rate': str(obj.interest_rate),
            'status': obj.status,
            'status_display': obj.get_status_display(),
            'approved_by_id': obj.approved_by_id,
            'approved_by_name': obj.approved_by.full_name if obj.approved_by else None,
            'purpose_notes': obj.purpose_notes,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [LoanSerializer.serialize(obj) for obj in queryset]


class LoanRepaymentSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'loan_id': obj.loan_id,
            'repayment_date': obj.repayment_date.isoformat(),
            'amount': str(obj.amount),
            'principal_amount': str(obj.principal_amount),
            'interest_amount': str(obj.interest_amount),
            'remaining_balance': str(obj.remaining_balance),
            'created_at': obj.created_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [LoanRepaymentSerializer.serialize(obj) for obj in queryset]
