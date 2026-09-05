from core_module.abstract.base_service import BaseService
from core_module.repository.onboarding.onboarding_repository import ExitInterviewRepository


class ExitInterviewService(BaseService):
    def __init__(self):
        super().__init__(ExitInterviewRepository())
