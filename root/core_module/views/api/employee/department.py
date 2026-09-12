"""
@module views/api/employee/department
@description Department CRUD and list routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.employee.department import DepartmentService
from core_module.serializers.employee.department import DepartmentSerializer

department_service = DepartmentService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@require_login
@safe_json_handler
@require_http_methods(["GET", "POST"])
def department_list(request):
    if request.method == "GET":
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        search = request.GET.get('search', '').strip()
        sort_by = request.GET.get('sort_by', 'name')
        sort_direction = request.GET.get('sort_direction', 'asc')
        has_pagination = 'page' in request.GET or 'page_size' in request.GET
        if search:
            qs = department_service.repository.search_departments(search)
        else:
            qs = department_service.get_all()
        allowed_sort = {
            'id': 'id',
            'name': 'name',
            'created_at': 'created_at',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='name')
        if has_pagination:
            _, _, _, page, page_size = parse_pagination_params(request, default_sort='name', default_direction='asc')
            page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
            return JsonResponse({
                'data': DepartmentSerializer.serialize_list(page_qs),
                'count': total,
                'page': page,
                'page_size': page_size,
                'total_pages': total_pages,
                'sort_by': sort_by,
                'sort_direction': sort_direction,
            })
        return JsonResponse({'data': DepartmentSerializer.serialize_list(qs), 'count': qs.count()})

    data = parse_body(request)
    instance, errors = department_service.create(**data)
    if instance:
        return JsonResponse(DepartmentSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@require_login
@safe_json_handler
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
