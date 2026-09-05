from core_module.abstract.base_service import BaseService
from core_module.repository.employee.employee_repository import LocationRepository


class LocationService(BaseService):
    def __init__(self):
        super().__init__(LocationRepository())
