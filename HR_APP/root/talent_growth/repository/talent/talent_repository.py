from django.db.models import Q
from core_module.abstract.base_repository import BaseRepository
from talent_growth.models.talent_growth.talent_growth import TalentProfile, SuccessionPlan


class TalentProfileRepository(BaseRepository):
    def __init__(self):
        super().__init__(TalentProfile)

    def get_by_potential(self, potential):
        return self.model.objects.filter(potential=potential)

    def get_high_potentials(self):
        return self.model.objects.filter(potential='high')

    def get_ready_now(self):
        return self.model.objects.filter(readiness='ready_now')

    def search_profiles(self, query):
        return self.model.objects.filter(
            Q(employee_name__icontains=query) |
            Q(current_role__icontains=query) |
            Q(next_role__icontains=query) |
            Q(development_areas__icontains=query)
        )


class SuccessionPlanRepository(BaseRepository):
    def __init__(self):
        super().__init__(SuccessionPlan)

    def get_active_plans(self):
        return self.model.objects.filter(is_active=True)

    def get_by_department(self, department_id):
        return self.model.objects.filter(department_id=department_id)

    def get_high_risk(self):
        return self.model.objects.filter(readiness_level__in=['immediate', '1_year'])

    def get_by_status(self, status):
        return self.model.objects.filter(status=status)

    def search_plans(self, query):
        return self.model.objects.filter(
            Q(position__icontains=query) |
            Q(incumbent_name__icontains=query) |
            Q(successor1_name__icontains=query)
        )
