import json
import traceback

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core_module.services.employee.employee_service import (
    EmployeeService, DepartmentService, LocationService, DesignationService, DocumentService
)
from core_module.serializers.employee_serializers import (
    EmployeeSerializer, DepartmentSerializer, LocationSerializer, DesignationSerializer, DocumentSerializer
)

employee_service = EmployeeService()
department_service = DepartmentService()
location_service = LocationService()
designation_service = DesignationService()
document_service = DocumentService()


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


# Department APIs
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


# Location APIs
@csrf_exempt
@require_http_methods(["GET", "POST"])
def location_list(request):
    if request.method == "GET":
        qs = location_service.get_all()
        return JsonResponse({'data': LocationSerializer.serialize_list(qs), 'count': qs.count()})
    data = parse_body(request)
    instance, errors = location_service.create(**data)
    if instance:
        return JsonResponse(LocationSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def location_detail(request, pk):
    if request.method == "GET":
        instance = location_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(LocationSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        instance, errors = location_service.update(pk, **data)
        if instance:
            return JsonResponse(LocationSerializer.serialize(instance))
        return JsonResponse({'errors': errors}, status=400)
    elif request.method == "DELETE":
        success, errors = location_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)


# Designation APIs
@csrf_exempt
@require_http_methods(["GET", "POST"])
def designation_list(request):
    if request.method == "GET":
        dept = request.GET.get('department')
        if dept:
            qs = designation_service.repository.get_by_department(dept)
        else:
            qs = designation_service.get_all()
        return JsonResponse({'data': DesignationSerializer.serialize_list(qs), 'count': qs.count()})
    data = parse_body(request)
    instance, errors = designation_service.create(**data)
    if instance:
        return JsonResponse(DesignationSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def designation_detail(request, pk):
    if request.method == "GET":
        instance = designation_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(DesignationSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        instance, errors = designation_service.update(pk, **data)
        if instance:
            return JsonResponse(DesignationSerializer.serialize(instance))
        return JsonResponse({'errors': errors}, status=400)
    elif request.method == "DELETE":
        success, errors = designation_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)


# Employee APIs
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
    # Convert FK fields: rename to _id suffix and convert to int
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
        # Convert FK fields: rename to _id suffix and convert to int
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


# Document APIs
@csrf_exempt
@require_http_methods(["GET", "POST"])
def document_list(request):
    if request.method == "GET":
        employee_id = request.GET.get('employee')
        if employee_id:
            qs = document_service.get_by_employee(employee_id)
        else:
            qs = document_service.get_all()
        return JsonResponse({'data': DocumentSerializer.serialize_list(qs), 'count': qs.count()})
    data = parse_body(request)
    instance, errors = document_service.create(**data)
    if instance:
        return JsonResponse(DocumentSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)