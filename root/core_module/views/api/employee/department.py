"""
@module views/api/employee/department
@description Department CRUD and list routes
"""
import json
import traceback

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core_module.services.employee.employee_service import DepartmentService
from core_module.serializers.employee_serializers import DepartmentSerializer

department_service = DepartmentService()


def safe_json_handler(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as exc:
            tb = traceback.format_exc()
            return JsonResponse({'error': str(exc), 'traceback': tb}, status=500)
    return _wrapped_view


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@csrf_exempt
@require_http_methods(["GET", "POST"])
@safe_json_handler
def department_list(request):
    if request.method == "GET":
        search = request.GET.get('search', '')
        if search:
            qs = department_service.repository.search_departments(search)
        else:
            qs = department_service.get_all()
        return JsonResponse({'data': DepartmentSerializer.serialize_list(qs), 'count': qs.count()})
    
    data = parse_body(request)
    instance, errors = department_service.create(**data)
    if instance:
        return JsonResponse(DepartmentSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def department_detail(request, pk):
    if request.method == "GET":
        instance = department_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(DepartmentSerializer.serialize(instance))
    
    elif request.method == "PUT":
        data = parse_body(request)
        instance, errors = department_service.update(pk, **data)
        if instance:
            return JsonResponse(DepartmentSerializer.serialize(instance))
        return JsonResponse({'errors': errors}, status=400)
    
    elif request.method == "DELETE":
        success, errors = department_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)
