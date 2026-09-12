"""
@module views/api/payroll/structure
@description Salary structure CRUD and list routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.payroll.structure import SalaryStructureService
from core_module.serializers.payroll.structure import SalaryStructureSerializer

salary_service = SalaryStructureService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@require_login
@safe_json_handler
@require_http_methods(["GET", "POST"])
def salary_structure_list(request):
    if request.method == "GET":
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
            'structure_name': 'structure_name',
            'basic_salary': 'basic_salary',
            'grade_level': 'grade_level',
            'created_at': 'created_at',
        }
        sort_field = allowed_sort.get(sort_by, 'id')
        if sort_direction not in ['asc', 'desc']:
            sort_direction = 'desc'
        ordering = sort_field if sort_direction == 'asc' else f'-{sort_field}'

        qs = salary_service.get_active()
        if search:
            from django.db.models import Q
            qs = qs.filter(
                Q(structure_name__icontains=search) |
                Q(grade_level__icontains=search)
            )
        qs = qs.order_by(ordering)
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]

        return JsonResponse({
            'data': SalaryStructureSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })

    data = parse_body(request)

    try:
        instance, errors = salary_service.create(**data)

        if instance:
            return JsonResponse(SalaryStructureSerializer.serialize(instance), status=201)

        return JsonResponse({'errors': errors}, status=400)
    except Exception as e:
        return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)


@require_login
@safe_json_handler
@require_http_methods(["GET", "PUT", "DELETE"])
def salary_structure_detail(request, pk):
    if request.method == "GET":
        instance = salary_service.get_by_id(pk)

        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)

        return JsonResponse(SalaryStructureSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)

        try:
            instance, errors = salary_service.update(pk, **data)

            if instance:
                return JsonResponse(SalaryStructureSerializer.serialize(instance))

            return JsonResponse({'errors': errors}, status=400)
        except Exception as e:
            return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)
    elif request.method == "DELETE":
        success, errors = salary_service.delete(pk)

        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
            
        return JsonResponse({'errors': errors}, status=404)
