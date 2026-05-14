from core_module.abstract.base_service import BaseService
from operation.repository.audit_repository import AuditLogRepository


class AuditLogService(BaseService):
    def __init__(self):
        super().__init__(AuditLogRepository())

    def log(self, user, action, model_name, object_id='', changes='', ip_address=None):
        return self.repository.log_action(user, action, model_name, object_id, changes, ip_address)

    def get_by_model(self, model_name):
        return self.repository.get_by_model(model_name)
