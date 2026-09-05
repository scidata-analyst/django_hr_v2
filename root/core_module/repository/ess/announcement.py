from core_module.abstract.base_repository import BaseRepository
from core_module.models.ess.announcement import Announcement


class AnnouncementRepository(BaseRepository):
    def __init__(self):
        super().__init__(Announcement)

    def get_active_announcements(self):
        from django.utils import timezone
        return self.model.objects.filter(
            is_active=True
        ).exclude(
            expires_at__lt=timezone.now()
        ).order_by('-is_pinned', '-published_at')

    def get_pinned(self):
        return self.model.objects.filter(is_pinned=True, is_active=True)
