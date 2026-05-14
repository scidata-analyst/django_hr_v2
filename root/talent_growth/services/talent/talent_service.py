from core_module.abstract.base_service import BaseService
from talent_growth.repository.talent.talent_repository import (
    TalentProfileRepository, SuccessionPlanRepository
)


class TalentProfileService(BaseService):
    def __init__(self):
        super().__init__(TalentProfileRepository())

    def get_high_potentials(self):
        return self.repository.get_high_potentials()

    def get_ready_now(self):
        return self.repository.get_ready_now()


class SuccessionPlanService(BaseService):
    def __init__(self):
        super().__init__(SuccessionPlanRepository())

    def create_plan(self, data):
        if 'secondary_successors' in data:
            secondary = data.pop('secondary_successors')
            plan = self.repository.create(**data)
            if secondary:
                plan.secondary_successors.set(secondary)
            return plan, {}
        return self.repository.create(**data), {}

    def get_active_plans(self):
        return self.repository.get_active_plans()
