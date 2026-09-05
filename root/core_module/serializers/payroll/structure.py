from core_module.models.payroll.structure import SalaryStructure


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
