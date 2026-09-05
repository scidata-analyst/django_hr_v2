from core_module.models.payroll.payslip import Payslip


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
