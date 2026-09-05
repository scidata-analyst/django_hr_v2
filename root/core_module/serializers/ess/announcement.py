from core_module.models.ess.announcement import Announcement


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
