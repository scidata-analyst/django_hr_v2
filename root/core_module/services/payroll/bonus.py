from core_module.abstract.base_service import BaseService
from core_module.repository.payroll.payroll_repository import BonusRepository


class BonusService(BaseService):
    def __init__(self):
        super().__init__(BonusRepository())

    def create_bonus(self, data):
        return self.repository.create(**data), {}
