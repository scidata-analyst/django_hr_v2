from core_module.abstract.base_service import BaseService
from core_module.repository.onboarding.onboarding_repository import (
    OnboardingTaskRepository, OffboardingTaskRepository, ExitInterviewRepository
)


class OnboardingTaskService(BaseService):
    def __init__(self):
        super().__init__(OnboardingTaskRepository())

    def create_onboarding_checklist(self, employee_id):
        task_types = [
            ('offer_letter', 'Sign Offer Letter'),
            ('document_verification', 'Document Verification'),
            ('it_setup', 'IT Equipment Setup'),
            ('orientation', 'Orientation Session'),
            ('team_introduction', 'Team Introduction'),
            ('training', 'Initial Training'),
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

    def get_by_employee(self, employee_id):
        return self.repository.get_by_employee(employee_id)

    def get_pending_tasks(self):
        return self.repository.get_pending_tasks()


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


class ExitInterviewService(BaseService):
    def __init__(self):
        super().__init__(ExitInterviewRepository())
