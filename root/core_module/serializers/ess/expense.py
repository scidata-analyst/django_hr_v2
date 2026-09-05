from core_module.models.ess.expense import ExpenseClaim


class ExpenseClaimSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'employee_id': obj.employee_id,
            'employee_name': obj.employee.full_name,
            'category': obj.category,
            'category_display': obj.get_category_display(),
            'amount': str(obj.amount),
            'expense_date': obj.expense_date.isoformat(),
            'description': obj.description,
            'receipt': obj.receipt.url if obj.receipt else None,
            'status': obj.status,
            'status_display': obj.get_status_display(),
            'approved_by_id': obj.approved_by_id,
            'approved_by_name': obj.approved_by.full_name if obj.approved_by else None,
            'approved_at': obj.approved_at.isoformat() if obj.approved_at else None,
            'rejection_reason': obj.rejection_reason,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [ExpenseClaimSerializer.serialize(obj) for obj in queryset]
