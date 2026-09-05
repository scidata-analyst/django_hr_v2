from core_module.abstract.base_repository import BaseRepository
from core_module.models.attendance.attendance import LeaveRequest


class LeaveRequestRepository(BaseRepository):
    def __init__(self):
        super().__init__(LeaveRequest)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def get_pending_requests(self):
        return self.model.objects.filter(status='pending')

    def get_by_status(self, status):
        return self.model.objects.filter(status=status)

    def check_overlapping_leave(self, employee_id, from_date, to_date, exclude_id=None):
        qs = self.model.objects.filter(
            employee_id=employee_id, status='approved',
            from_date__lte=to_date, to_date__gte=from_date
        )
        if exclude_id:
            qs = qs.exclude(pk=exclude_id)
        return qs.exists()
