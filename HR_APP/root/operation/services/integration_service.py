from core_module.abstract.base_service import BaseService
from operation.repository.integration_repository import IntegrationRepository


class IntegrationService(BaseService):
    def __init__(self):
        super().__init__(IntegrationRepository())

    def get_active(self):
        return self.repository.get_active()

    def toggle_integration(self, integration_id):
        integration = self.repository.read(integration_id)
        if integration is None:
            return None, {'error': 'Integration not found'}
        integration.is_enabled = not integration.is_enabled
        integration.status = 'active' if integration.is_enabled else 'inactive'
        integration.save()
        return integration, {}
