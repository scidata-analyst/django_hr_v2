import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core_module.services.attendance.attendance_service import (
    ShiftService, AttendanceService, LeaveRequestService
)
from core_module.serializers.attendance_serializers import (
    ShiftSerializer, AttendanceSerializer, LeaveRequestSerializer
)

shift_service = ShiftService()
attendance_service = AttendanceService()
leave_service = LeaveRequestService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@csrf_exempt
@require_http_methods(["GET", "POST"])
def shift_list(request):
    if request.method == "GET":
        qs = shift_service.get_active_shifts()
        return JsonResponse({'data': ShiftSerializer.serialize_list(qs), 'count': qs.count()})
    data = parse_body(request)
    instance, errors = shift_service.create(**data)
    if instance:
        return JsonResponse(ShiftSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def shift_detail(request, pk):
    if request.method == "GET":
        instance = shift_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(ShiftSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        instance, errors = shift_service.update(pk, **data)
        if instance:
            return JsonResponse(ShiftSerializer.serialize(instance))
        return JsonResponse({'errors': errors}, status=400)
    elif request.method == "DELETE":
        success, errors = shift_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)


@csrf_exempt
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
            from datetime import date as dt
            qs = attendance_service.repository.get_by_date(dt.today())
        
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


@csrf_exempt
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


def attendance_stats(request):
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    stats = attendance_service.get_attendance_stats(start, end)
    return JsonResponse(stats)


def employee_attendance_stats(request, employee_id):
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    stats = attendance_service.get_employee_stats(employee_id, start, end)
    return JsonResponse(stats)


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
@require_http_methods(["POST"])
def leave_approve(request, pk):
    data = parse_body(request)
    approved_by_id = data.get('approved_by_id')
    instance, errors = leave_service.approve_leave(pk, approved_by_id)
    if instance:
        return JsonResponse(LeaveRequestSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def leave_deny(request, pk):
    data = parse_body(request)
    approved_by_id = data.get('approved_by_id')
    denial_reason = data.get('denial_reason', '')
    instance, errors = leave_service.deny_leave(pk, approved_by_id, denial_reason)
    if instance:
        return JsonResponse(LeaveRequestSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)