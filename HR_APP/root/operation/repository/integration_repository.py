from core_module.abstract.base_repository import BaseRepository
from operation.models.operation.operation import Integration


class IntegrationRepository(BaseRepository):
    def __init__(self):
        super().__init__(Integration)

    def get_active(self):
        return self.model.objects.filter(is_enabled=True, status='active')

    def get_by_type(self, integration_type):
        return self.model.objects.filter(integration_type=integration_type)
