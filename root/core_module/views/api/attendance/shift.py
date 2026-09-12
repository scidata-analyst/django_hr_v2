"""
@module views/api/attendance/shift
@description Shift CRUD and list routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.attendance.shift import ShiftService
from core_module.serializers.attendance.shift import ShiftSerializer

shift_service = ShiftService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


def _normalize_fk(data):
    """Normalize FK string IDs to int and map `field` -> `field_id` for Shift (department)."""
    for fk in ['department']:
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
def shift_list(request):
    if request.method == "GET":
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        search = request.GET.get('search', '').strip()
        sort_by = request.GET.get('sort_by', 'id')
        sort_direction = request.GET.get('sort_direction', 'desc')
        # Support both paginated and non-paginated (dropdown) usage
        has_pagination = 'page' in request.GET or 'page_size' in request.GET
        if has_pagination:
            _, _, _, page, page_size = parse_pagination_params(request, default_sort='id')
        else:
            page, page_size = 1, 100
            # still parse sort/search
            search = request.GET.get('search', '').strip()
            sort_by = request.GET.get('sort_by', 'id')
            sort_direction = request.GET.get('sort_direction', 'desc')

        qs = shift_service.get_active_shifts()
        if search:
            from django.db.models import Q
            qs = qs.filter(
                Q(shift_name__icontains=search) |
                Q(shift_code__icontains=search) |
                Q(working_days__icontains=search)
            )
        allowed_sort = {
            'id': 'id',
            'shift_name': 'shift_name',
            'shift_code': 'shift_code',
            'start_time': 'start_time',
            'created_at': 'created_at',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='id')
        if has_pagination:
            page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
            return JsonResponse({
                'data': ShiftSerializer.serialize_list(page_qs),
                'count': total,
                'page': page,
                'page_size': page_size,
                'total_pages': total_pages,
                'sort_by': sort_by,
                'sort_direction': sort_direction,
            })
        return JsonResponse({'data': ShiftSerializer.serialize_list(qs), 'count': qs.count()})
    data = parse_body(request)
    data = _normalize_fk(data)
    instance, errors = shift_service.create(**data)
    if instance:
        return JsonResponse(ShiftSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@require_login
@safe_json_handler
@require_http_methods(["GET", "PUT", "DELETE"])
def shift_detail(request, pk):
    if request.method == "GET":
        instance = shift_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(ShiftSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        data = _normalize_fk(data)
        instance, errors = shift_service.update(pk, **data)
        if instance:
            return JsonResponse(ShiftSerializer.serialize(instance))
        return JsonResponse({'errors': errors}, status=400)
    elif request.method == "DELETE":
        success, errors = shift_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)
