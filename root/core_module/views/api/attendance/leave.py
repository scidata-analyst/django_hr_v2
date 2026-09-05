"""
@module views/api/attendance/leave
@description Leave request CRUD, approve and deny routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.attendance.leave import LeaveRequestService
from core_module.serializers.attendance.leave import LeaveRequestSerializer

leave_service = LeaveRequestService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@require_login
@safe_json_handler
@require_http_methods(["GET", "POST"])
def leave_list(request):
    if request.method == "GET":
        status = request.GET.get('status')
        employee = request.GET.get('employee')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        if status:
            qs = leave_service.repository.get_by_status(status)
        elif employee:
            qs = leave_service.get_by_employee(employee)
        else:
            qs = leave_service.get_all()

        qs = qs.select_related('employee', 'approved_by')

        total = qs.count()
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_qs = qs[start_idx:end_idx]

        return JsonResponse({
            'data': LeaveRequestSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })

    data = parse_body(request)
    try:
        instance, errors = leave_service.apply_leave(data)
        if instance:
            return JsonResponse(LeaveRequestSerializer.serialize(instance), status=201)
        return JsonResponse({'errors': errors}, status=400)
    except Exception as e:
        return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)


@require_login
@safe_json_handler
@require_http_methods(["GET", "PUT", "DELETE"])
def leave_detail(request, pk):
    if request.method == "GET":
        instance = leave_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(LeaveRequestSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        instance, errors = leave_service.update(pk, **data)
        if instance:
            return JsonResponse(LeaveRequestSerializer.serialize(instance))
        return JsonResponse({'errors': errors}, status=400)
    elif request.method == "DELETE":
        success, errors = leave_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)


@require_login
@safe_json_handler
@require_http_methods(["POST"])
def leave_approve(request, pk):
    data = parse_body(request)
    approved_by_id = data.get('approved_by_id')
    instance, errors = leave_service.approve_leave(pk, approved_by_id)
    if instance:
        return JsonResponse(LeaveRequestSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)


@require_login
@safe_json_handler
@require_http_methods(["POST"])
def leave_deny(request, pk):
    data = parse_body(request)
    approved_by_id = data.get('approved_by_id')
    denial_reason = data.get('denial_reason', '')
    instance, errors = leave_service.deny_leave(pk, approved_by_id, denial_reason)
    if instance:
        return JsonResponse(LeaveRequestSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)
