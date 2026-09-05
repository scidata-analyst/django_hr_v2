from core_module.abstract.base_repository import BaseRepository
from core_module.models.employee.designation import Designation


class DesignationRepository(BaseRepository):
    def __init__(self):
        super().__init__(Designation)

    def get_by_department(self, department_id):
        return self.model.objects.filter(department_id=department_id)

    def get_by_level(self, level):
        return self.model.objects.filter(level=level)
