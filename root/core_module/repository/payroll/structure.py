from core_module.abstract.base_repository import BaseRepository
from core_module.models.payroll.payroll import SalaryStructure


class SalaryStructureRepository(BaseRepository):
    def __init__(self):
        super().__init__(SalaryStructure)

    def get_active(self):
        return self.model.objects.filter(is_active=True)
