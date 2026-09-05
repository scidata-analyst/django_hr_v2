from datetime import date
from core_module.abstract.base_repository import BaseRepository
from core_module.models.employee.employee import Document


class DocumentRepository(BaseRepository):
    def __init__(self):
        super().__init__(Document)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def get_by_type(self, document_type):
        return self.model.objects.filter(document_type=document_type)

    def get_pending_documents(self):
        return self.model.objects.filter(status='pending')

    def get_expired_documents(self):
        return self.model.objects.filter(expiry_date__lt=date.today(), status='verified')
