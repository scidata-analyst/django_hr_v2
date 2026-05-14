from django.db.models import Q
from core_module.abstract.base_repository import BaseRepository
from operation.models.operation.operation import BenefitPlan, BenefitEnrollment


class BenefitPlanRepository(BaseRepository):
    def __init__(self):
        super().__init__(BenefitPlan)

    def get_active_plans(self):
        return self.model.objects.filter(is_active=True)

    def get_by_type(self, plan_type):
        return self.model.objects.filter(plan_type=plan_type)

    def search_plans(self, query):
        return self.model.objects.filter(
            Q(plan_name__icontains=query) |
            Q(plan_type__icontains=query) |
            Q(coverage_details__icontains=query)
        )

    def get_by_status(self, status):
        if status == 'active':
            return self.model.objects.filter(is_active=True)
        return self.model.objects.filter(is_active=False)


class BenefitEnrollmentRepository(BaseRepository):
    def __init__(self):
        super().__init__(BenefitEnrollment)

    def get_by_employee(self, employee_id):
        return self.model.objects.filter(employee_id=employee_id)

    def get_by_plan(self, plan_id):
        return self.model.objects.filter(plan_id=plan_id)

    def get_active_enrollments(self):
        return self.model.objects.filter(status='active')
