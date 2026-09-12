"""
@module views/api/employee/location
@description Location CRUD and list routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.employee.location import LocationService
from core_module.serializers.employee.location import LocationSerializer

location_service = LocationService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@require_login
@safe_json_handler
@require_http_methods(["GET", "POST"])
def location_list(request):
    if request.method == "GET":
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        search = request.GET.get('search', '').strip()
        sort_by = request.GET.get('sort_by', 'name')
        sort_direction = request.GET.get('sort_direction', 'asc')
        has_pagination = 'page' in request.GET or 'page_size' in request.GET

        qs = location_service.get_all()
        if search:
            from django.db.models import Q
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(city__icontains=search) |
                Q(country__icontains=search) |
                Q(location_type__icontains=search)
            )
        allowed_sort = {
            'id': 'id',
            'name': 'name',
            'city': 'city',
            'country': 'country',
            'created_at': 'created_at',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='name')
        if has_pagination:
            _, _, _, page, page_size = parse_pagination_params(request, default_sort='name', default_direction='asc')
            page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
            return JsonResponse({
                'data': LocationSerializer.serialize_list(page_qs),
                'count': total,
                'page': page,
                'page_size': page_size,
                'total_pages': total_pages,
                'sort_by': sort_by,
                'sort_direction': sort_direction,
            })
        return JsonResponse({'data': LocationSerializer.serialize_list(qs), 'count': qs.count()})
    data = parse_body(request)
    instance, errors = location_service.create(**data)
    if instance:
        return JsonResponse(LocationSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@require_login
@safe_json_handler
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
