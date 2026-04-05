from core_module.models.ess.ess import ExpenseClaim, Announcement


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


class AnnouncementSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'title': obj.title,
            'content': obj.content,
            'priority': obj.priority,
            'priority_display': obj.get_priority_display(),
            'is_pinned': obj.is_pinned,
            'published_by_id': obj.published_by_id,
            'published_by_name': obj.published_by.full_name if obj.published_by else None,
            'published_at': obj.published_at.isoformat(),
            'expires_at': obj.expires_at.isoformat() if obj.expires_at else None,
            'is_active': obj.is_active,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [AnnouncementSerializer.serialize(obj) for obj in queryset]
