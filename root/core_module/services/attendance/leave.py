from django.db import IntegrityError
from core_module.abstract.base_service import BaseService
from core_module.repository.attendance.leave import LeaveRequestRepository


class LeaveRequestService(BaseService):
    def __init__(self):
        super().__init__(LeaveRequestRepository())

    def validate(self, **kwargs):
        errors = {}
        from_date = kwargs.get('from_date')
        to_date = kwargs.get('to_date')
        if from_date and to_date and from_date > to_date:
            errors['to_date'] = 'To date must be after from date.'
        employee_id = kwargs.get('employee_id')
        if employee_id and from_date and to_date:
            if self.repository.check_overlapping_leave(
                employee_id, from_date, to_date, kwargs.get('pk')
            ):
                errors['date'] = 'Overlapping approved leave exists for these dates.'
        return len(errors) == 0, errors

    def apply_leave(self, data):
        is_valid, errors = self.validate(**data)
        if not is_valid:
            return None, errors
        try:
            leave = self.repository.create(**data)
            return leave, {}
        except IntegrityError as e:
            return None, {'error': str(e)}

    def approve_leave(self, leave_id, approved_by_id):
        leave = self.repository.read(leave_id)
        if not leave:
            return None, {'error': 'Leave request not found'}
        if leave.status != 'pending':
            return None, {'error': 'Leave request is not pending'}
        from django.utils import timezone
        leave.status = 'approved'
        leave.approved_by_id = approved_by_id
        leave.approved_at = timezone.now()
        leave.save()
        return leave, {}

    def deny_leave(self, leave_id, approved_by_id, denial_reason=''):
        leave = self.repository.read(leave_id)
        if not leave:
            return None, {'error': 'Leave request not found'}
        if leave.status != 'pending':
            return None, {'error': 'Leave request is not pending'}
        leave.status = 'denied'
        leave.approved_by_id = approved_by_id
        leave.denial_reason = denial_reason
        leave.save()
        return leave, {}

    def get_pending_requests(self):
        return self.repository.get_pending_requests()

    def get_by_employee(self, employee_id):
        return self.repository.get_by_employee(employee_id)
