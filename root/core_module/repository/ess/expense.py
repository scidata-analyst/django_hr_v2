from django.db.models import Sum
from core_module.abstract.base_repository import BaseRepository
from core_module.models.ess.expense import ExpenseClaim


class ExpenseClaimRepository(BaseRepository):
    def __init__(self):
        super().__init__(ExpenseClaim)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def get_pending_claims(self):
        return self.model.objects.filter(status='pending')

    def get_by_status(self, status):
        return self.model.objects.filter(status=status)

    def get_employee_pending_total(self, employee_id):
        return self.model.objects.filter(
            employee_id=employee_id, status='pending'
        ).aggregate(total=Sum('amount'))['total'] or 0
