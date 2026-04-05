from core_module.abstract.base_repository import BaseRepository
from operation.models.operation.operation import AuditLog


class AuditLogRepository(BaseRepository):
    def __init__(self):
        super().__init__(AuditLog)

    def log_action(self, user, action, model_name, object_id='', changes='', ip_address=None):
        return self.model.objects.create(
            user=user, action=action, model_name=model_name,
            object_id=str(object_id), changes=changes, ip_address=ip_address
        )

    def get_by_model(self, model_name):
        return self.model.objects.filter(model_name=model_name)

    def get_by_user(self, user_id):
        return self.model.objects.filter(user_id=user_id)

    def get_by_action(self, action):
        return self.model.objects.filter(action=action)
