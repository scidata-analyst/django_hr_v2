from django.db.models import Q
from core_module.abstract.base_repository import BaseRepository
from operation.models.global_.global_ import Office


class OfficeRepository(BaseRepository):
    def __init__(self):
        super().__init__(Office)

    def get_by_country(self, country):
        return self.model.objects.filter(country=country)

    def get_by_status(self, status):
        return self.model.objects.filter(status=status)

    def search_offices(self, query):
        return self.search(['name', 'country', 'city', 'office_type'], query)
