"""
@module views/api/attendance/attendance_api
@description Attendance CRUD and stats routes
"""
import json
from datetime import date as dt

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.attendance.attendance import AttendanceService
from core_module.serializers.attendance.attendance import AttendanceSerializer

attendance_service = AttendanceService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


def _normalize_fk(data):
    """Normalize FK string IDs to int and map `field` -> `field_id` for Attendance (employee, shift)."""
    for fk in ['employee', 'shift']:
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
def attendance_list(request):
    if request.method == "GET":
        date = request.GET.get('date')
        employee = request.GET.get('employee')
        start = request.GET.get('start_date')
        end = request.GET.get('end_date')
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
            'date': 'date',
            'status': 'status',
            'created_at': 'created_at',
            'employee': 'employee_id',
        }
        sort_field = allowed_sort.get(sort_by, 'id')
        if sort_direction not in ['asc', 'desc']:
            sort_direction = 'desc'
        ordering = sort_field if sort_direction == 'asc' else f'-{sort_field}'

        if search:
            from django.db.models import Q
            qs = attendance_service.get_all().filter(
                Q(employee__first_name__icontains=search) |
                Q(employee__last_name__icontains=search) |
                Q(employee__employee_id__icontains=search) |
                Q(status__icontains=search)
            )
        elif employee and start and end:
            qs = attendance_service.repository.get_by_employee_and_date_range(employee, start, end)
        elif date:
            qs = attendance_service.repository.get_by_date(date)
        elif employee:
            qs = attendance_service.repository.get_by_employee(employee)
        else:
            qs = attendance_service.repository.get_by_date(dt.today())

        qs = qs.select_related('employee', 'shift').order_by(ordering)

        total = qs.count()
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_qs = qs[start_idx:end_idx]

        return JsonResponse({
            'data': AttendanceSerializer.serialize_list(page_qs),
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
        instance, errors = attendance_service.mark_attendance(data)
        if instance:
            return JsonResponse(AttendanceSerializer.serialize(instance), status=201)
        return JsonResponse({'errors': errors}, status=400)
    except Exception as e:
        return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)


@require_login
@safe_json_handler
@require_http_methods(["GET", "PUT", "DELETE"])
def attendance_detail(request, pk):
    if request.method == "GET":
        instance = attendance_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(AttendanceSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        data = _normalize_fk(data)
        instance, errors = attendance_service.update(pk, **data)
        if instance:
            return JsonResponse(AttendanceSerializer.serialize(instance))
        return JsonResponse({'errors': errors}, status=400)
    elif request.method == "DELETE":
        success, errors = attendance_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)


@require_login
@safe_json_handler
def attendance_stats(request):
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    stats = attendance_service.get_attendance_stats(start, end)
    return JsonResponse(stats)


@require_login
@safe_json_handler
def employee_attendance_stats(request, employee_id):
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    stats = attendance_service.get_employee_stats(employee_id, start, end)
    return JsonResponse(stats)
