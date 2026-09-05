from core_module.abstract.base_service import BaseService
from core_module.repository.ess.ess_repository import AnnouncementRepository


class AnnouncementService(BaseService):
    def __init__(self):
        super().__init__(AnnouncementRepository())

    def get_active_announcements(self):
        return self.repository.get_active_announcements()

    def publish(self, data):
        return self.repository.create(**data), {}
