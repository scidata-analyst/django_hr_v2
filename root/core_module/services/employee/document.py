from core_module.abstract.base_service import BaseService
from core_module.repository.employee.document import DocumentRepository


class DocumentService(BaseService):
    def __init__(self):
        super().__init__(DocumentRepository())

    def get_by_employee(self, employee_id):
        return self.repository.get_by_employee(employee_id)
