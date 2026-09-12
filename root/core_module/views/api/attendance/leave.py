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


def _normalize_fk(data):
    """Normalize FK string IDs to int and map `field` -> `field_id` for Leave (employee, approved_by)."""
    for fk in ['employee', 'approved_by']:
        id_key = f"{fk}_id"
        for key in (fk, id_key):
            if key in data and isinstance(data[key], str):
                val = data[key].strip()
                if val == '':
                    data[key] = None
                else:
                    try:
                        data[key] = int(val)
                    except (ValueError, TypeError):
                        pass
        if fk in data:
            val = data.pop(fk)
            if id_key not in data or data[id_key] is None or data[id_key] == '':
                data[id_key] = val
        if id_key in data and isinstance(data[id_key], str):
            try:
                data[id_key] = int(data[id_key].strip()) if data[id_key].strip() != '' else None
            except (ValueError, TypeError):
                data[id_key] = None
        if data.get(id_key) == '':
            data[id_key] = None
    return data


@require_login
@safe_json_handler
@require_http_methods(["GET", "POST"])
def leave_list(request):
    if request.method == "GET":
        status = request.GET.get('status')
        employee = request.GET.get('employee')
        search = request.GET.get('search', '').strip()
        sort_by = request.GET.get('sort_by', 'id')
        sort_direction = request.GET.get('sort_direction', 'desc')
        try:
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            if page < 1:
                page = 1
            if page_size < 1:
                page_size = 10
            if page_size > 100:
                page_size = 100
        except (ValueError, TypeError):
            page, page_size = 1, 10

        allowed_sort = {
            'id': 'id',
            'from_date': 'from_date',
            'to_date': 'to_date',
            'status': 'status',
            'created_at': 'created_at',
            'leave_type': 'leave_type',
        }
        sort_field = allowed_sort.get(sort_by, 'id')
        if sort_direction not in ['asc', 'desc']:
            sort_direction = 'desc'
        ordering = sort_field if sort_direction == 'asc' else f'-{sort_field}'

        if search:
            from django.db.models import Q
            qs = leave_service.get_all().filter(
                Q(employee__first_name__icontains=search) |
                Q(employee__last_name__icontains=search) |
                Q(employee__employee_id__icontains=search) |
                Q(leave_type__icontains=search) |
                Q(status__icontains=search) |
                Q(reason__icontains=search)
            )
        elif status:
            qs = leave_service.repository.get_by_status(status)
        elif employee:
            qs = leave_service.get_by_employee(employee)
        else:
            qs = leave_service.get_all()

        # Apply additional filters if both search and status/employee provided
        if search and status:
            qs = qs.filter(status=status)
        if search and employee:
            qs = qs.filter(employee_id=employee)

        qs = qs.select_related('employee', 'approved_by').order_by(ordering)

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
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })

    data = parse_body(request)
    data = _normalize_fk(data)
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
        data = _normalize_fk(data)
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
    data = _normalize_fk(data)
    approved_by_id = data.get('approved_by_id')
    # also handle approved_by string variant already normalized, but ensure int conversion for fallback
    if approved_by_id is None and 'approved_by' in data:
        approved_by_id = data.get('approved_by_id')
    if isinstance(approved_by_id, str):
        try:
            approved_by_id = int(approved_by_id.strip()) if approved_by_id.strip() != '' else None
        except (ValueError, TypeError):
            approved_by_id = None
    instance, errors = leave_service.approve_leave(pk, approved_by_id)
    if instance:
        return JsonResponse(LeaveRequestSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)


@require_login
@safe_json_handler
@require_http_methods(["POST"])
def leave_deny(request, pk):
    data = parse_body(request)
    data = _normalize_fk(data)
    approved_by_id = data.get('approved_by_id')
    if isinstance(approved_by_id, str):
        try:
            approved_by_id = int(approved_by_id.strip()) if approved_by_id.strip() != '' else None
        except (ValueError, TypeError):
            approved_by_id = None
    denial_reason = data.get('denial_reason', '')
    instance, errors = leave_service.deny_leave(pk, approved_by_id, denial_reason)
    if instance:
        return JsonResponse(LeaveRequestSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)


@require_login
@safe_json_handler
@require_http_methods(["GET"])
def leave_balance_stats(request):
    stats = leave_service.get_balance_stats()
    return JsonResponse(stats)
