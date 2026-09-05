from core_module.abstract.base_repository import BaseRepository
from core_module.models.payroll.payroll import Bonus


class BonusRepository(BaseRepository):
    def __init__(self):
        super().__init__(Bonus)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def get_by_month(self, pay_month):
        return self.model.objects.filter(pay_month=pay_month)

    def get_pending_bonuses(self):
        return self.model.objects.filter(status='pending')
