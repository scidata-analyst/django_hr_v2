from core_module.abstract.base_service import BaseService
from operation.repository.global_ import OfficeRepository


class OfficeService(BaseService):
    def __init__(self):
        super().__init__(OfficeRepository())

    def get_by_country(self, country):
        return self.repository.get_by_country(country)

    def get_by_status(self, status):
        return self.repository.get_by_status(status)

    def search_offices(self, query):
        return self.repository.search_offices(query)
