from core_module.abstract.base_service import BaseService
from core_module.repository.onboarding.onboarding_repository import OffboardingTaskRepository


class OffboardingTaskService(BaseService):
    def __init__(self):
        super().__init__(OffboardingTaskRepository())

    def create_offboarding_checklist(self, employee_id):
        task_types = [
            ('knowledge_transfer', 'Knowledge Transfer'),
            ('equipment_return', 'Return IT Equipment'),
            ('access_revocation', 'Revoke System Access'),
            ('clearance', 'Departmental Clearance'),
            ('final_settlement', 'Final Settlement'),
            ('exit_interview', 'Exit Interview'),
        ]
        tasks = []
        for task_type, task_name in task_types:
            task = self.repository.create(
                employee_id=employee_id,
                task_type=task_type,
                task_name=task_name,
                status='pending'
            )
            tasks.append(task)
        return tasks
