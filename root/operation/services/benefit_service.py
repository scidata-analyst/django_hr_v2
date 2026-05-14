from core_module.abstract.base_service import BaseService
from operation.repository.benefit_repository import BenefitPlanRepository, BenefitEnrollmentRepository


class BenefitPlanService(BaseService):
    def __init__(self):
        super().__init__(BenefitPlanRepository())

    def get_active_plans(self):
        return self.repository.get_active_plans()


class BenefitEnrollmentService(BaseService):
    def __init__(self):
        super().__init__(BenefitEnrollmentRepository())

    def enroll(self, data):
        return self.repository.create(**data), {}

    def get_by_employee(self, employee_id):
        return self.repository.get_by_employee(employee_id)
