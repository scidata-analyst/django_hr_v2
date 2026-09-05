from django.db.models import Count
from core_module.abstract.base_repository import BaseRepository
from core_module.models.employee.location import Location


class LocationRepository(BaseRepository):
    def __init__(self):
        super().__init__(Location)

    def get_active(self):
        return self.model.objects.filter(is_active=True).annotate(employee_count=Count('employee_set'))

    def get_by_type(self, location_type):
        return self.model.objects.filter(location_type=location_type).annotate(employee_count=Count('employee_set'))

    def get_all(self):
        return self.model.objects.annotate(employee_count=Count('employee_set'))
