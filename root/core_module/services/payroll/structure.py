from core_module.abstract.base_service import BaseService
from core_module.repository.payroll.structure import SalaryStructureRepository


class SalaryStructureService(BaseService):
    def __init__(self):
        super().__init__(SalaryStructureRepository())

    def get_active(self):
        return self.repository.get_active()
