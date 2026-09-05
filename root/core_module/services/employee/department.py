from core_module.abstract.base_service import BaseService
from core_module.repository.employee.department import DepartmentRepository


class DepartmentService(BaseService):
    def __init__(self):
        super().__init__(DepartmentRepository())
