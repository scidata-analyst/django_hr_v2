from django.db.models import Q
from core_module.abstract.base_repository import BaseRepository
from core_module.models.attendance.shift import Shift


class ShiftRepository(BaseRepository):
    def __init__(self):
        super().__init__(Shift)

    def get_active_shifts(self):
        return self.model.objects.filter(is_active=True)

    def get_by_department(self, department_id):
        return self.model.objects.filter(
            Q(department_id=department_id) | Q(department__isnull=True)
        )
