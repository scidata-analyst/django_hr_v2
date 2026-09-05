from core_module.models.payroll.bonus import Bonus


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
