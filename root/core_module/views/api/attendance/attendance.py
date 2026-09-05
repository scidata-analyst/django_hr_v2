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
from core_module.serializers.attendance_serializers import AttendanceSerializer

attendance_service = AttendanceService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@require_login
@safe_json_handler
@require_http_methods(["GET", "POST"])
def attendance_list(request):
    if request.method == "GET":
        date = request.GET.get('date')
        employee = request.GET.get('employee')
        start = request.GET.get('start_date')
        end = request.GET.get('end_date')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        if employee and start and end:
            qs = attendance_service.repository.get_by_employee_and_date_range(employee, start, end)
        elif date:
            qs = attendance_service.repository.get_by_date(date)
        elif employee:
            qs = attendance_service.repository.get_by_employee(employee)
        else:
            qs = attendance_service.repository.get_by_date(dt.today())

        qs = qs.select_related('employee', 'shift')

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
        })

    data = parse_body(request)
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
