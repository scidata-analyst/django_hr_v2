from core_module.models.payroll.payroll import SalaryStructure, Payslip, Loan, LoanRepayment, Bonus


class SalaryStructureSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'structure_name': obj.structure_name,
            'grade_level': obj.grade_level,
            'basic_salary': str(obj.basic_salary),
            'house_rent_percent': str(obj.house_rent_percent),
            'transport_allowance': str(obj.transport_allowance),
            'medical_allowance': str(obj.medical_allowance),
            'food_allowance': str(obj.food_allowance),
            'other_allowance': str(obj.other_allowance),
            'income_tax_percent': str(obj.income_tax_percent),
            'provident_fund_percent': str(obj.provident_fund_percent),
            'insurance_premium': str(obj.insurance_premium),
            'other_deductions': str(obj.other_deductions),
            'gross_salary': str(obj.gross_salary),
            'total_deductions': str(obj.total_deductions),
            'net_salary': str(obj.net_salary),
            'is_active': obj.is_active,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [SalaryStructureSerializer.serialize(obj) for obj in queryset]


class PayslipSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'employee_id': obj.employee_id,
            'employee_name': obj.employee.full_name,
            'employee_code': obj.employee.employee_id,
            'salary_structure_id': obj.salary_structure_id,
            'pay_period': obj.pay_period,
            'pay_date': obj.pay_date.isoformat(),
            'basic_salary': str(obj.basic_salary),
            'house_rent': str(obj.house_rent),
            'transport_allowance': str(obj.transport_allowance),
            'medical_allowance': str(obj.medical_allowance),
            'food_allowance': str(obj.food_allowance),
            'other_allowance': str(obj.other_allowance),
            'overtime_amount': str(obj.overtime_amount),
            'bonus_amount': str(obj.bonus_amount),
            'gross_salary': str(obj.gross_salary),
            'income_tax': str(obj.income_tax),
            'provident_fund': str(obj.provident_fund),
            'insurance_deduction': str(obj.insurance_deduction),
            'other_deductions': str(obj.other_deductions),
            'loan_emi': str(obj.loan_emi),
            'absent_deduction': str(obj.absent_deduction),
            'late_deduction': str(obj.late_deduction),
            'total_deductions': str(obj.total_deductions),
            'net_pay': str(obj.net_pay),
            'is_generated': obj.is_generated,
            'pdf_file': obj.pdf_file.url if obj.pdf_file else None,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [PayslipSerializer.serialize(obj) for obj in queryset]


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


class BonusSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'employee_id': obj.employee_id,
            'employee_name': obj.employee.full_name if obj.employee else 'All Employees',
            'is_all_employees': obj.is_all_employees,
            'bonus_type': obj.bonus_type,
            'bonus_type_display': obj.get_bonus_type_display(),
            'amount': str(obj.amount),
            'pay_month': obj.pay_month.isoformat() if obj.pay_month else None,
            'taxable': obj.taxable,
            'status': obj.status,
            'status_display': obj.get_status_display(),
            'approved_by_id': obj.approved_by_id,
            'approved_by_name': obj.approved_by.full_name if obj.approved_by else None,
            'remarks': obj.remarks,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [BonusSerializer.serialize(obj) for obj in queryset]
