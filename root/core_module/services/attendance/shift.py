from core_module.abstract.base_service import BaseService
from core_module.repository.attendance.shift import ShiftRepository


class ShiftService(BaseService):
    def __init__(self):
        super().__init__(ShiftRepository())

    def get_active_shifts(self):
        return self.repository.get_active_shifts()
