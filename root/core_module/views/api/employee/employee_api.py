import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core_module.services.employee.employee_service import EmployeeService
from core_module.serializers.employee_serializers import EmployeeSerializer

employee_service = EmployeeService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@csrf_exempt
@require_http_methods(["GET", "POST"])
def employee_list(request):
    if request.method == "GET":
        search = request.GET.get('search', '')
        status = request.GET.get('status')
        department = request.GET.get('department')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        qs = employee_service.get_all()
        
        if search:
            qs = employee_service.search(search)
        if status:
            qs = qs.filter(status=status)
        if department:
            qs = qs.filter(department_id=department)
        
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        
        return JsonResponse({
            'data': EmployeeSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    
    data = parse_body(request)
    for fk_field in ['department', 'designation', 'reporting_manager', 'office_location']:
        val = data.pop(fk_field, None)
        if val == '' or val is None:
            data[f'{fk_field}_id'] = None
        elif isinstance(val, str) and val.strip():
            try:
                data[f'{fk_field}_id'] = int(val)
            except (ValueError, TypeError):
                data[f'{fk_field}_id'] = None
        elif isinstance(val, int):
            data[f'{fk_field}_id'] = val
    try:
        instance, errors = employee_service.create_employee(data)
        if instance:
            return JsonResponse(EmployeeSerializer.serialize(instance), status=201)
        return JsonResponse({'errors': errors}, status=400)
    except Exception as e:
        return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def employee_detail_api(request, pk):
    if request.method == "GET":
        instance = employee_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(EmployeeSerializer.serialize_detail(instance))
    
    elif request.method == "PUT":
        data = parse_body(request)
        for fk_field in ['department', 'designation', 'reporting_manager', 'office_location']:
            val = data.pop(fk_field, None)
            if val == '' or val is None:
                data[f'{fk_field}_id'] = None
            elif isinstance(val, str) and val.strip():
                try:
                    data[f'{fk_field}_id'] = int(val)
                except (ValueError, TypeError):
                    data[f'{fk_field}_id'] = None
            elif isinstance(val, int):
                data[f'{fk_field}_id'] = val
        try:
            instance, errors = employee_service.update_employee(pk, data)
            if instance:
                return JsonResponse(EmployeeSerializer.serialize(instance))
            return JsonResponse({'errors': errors}, status=400)
        except Exception as e:
            return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)
    
    elif request.method == "DELETE":
        success, errors = employee_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)


def employee_stats(request):
    stats = employee_service.get_dashboard_stats()
    return JsonResponse(stats)
