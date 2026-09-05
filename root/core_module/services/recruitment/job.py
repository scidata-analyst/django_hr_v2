from core_module.abstract.base_service import BaseService
from core_module.repository.recruitment.recruitment_repository import JobPostingRepository


class JobPostingService(BaseService):
    def __init__(self):
        super().__init__(JobPostingRepository())

    def get_active_jobs(self):
        return self.repository.get_active_jobs()

    def search_jobs(self, query):
        return self.repository.search_jobs(query)
