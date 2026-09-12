"""
@module views/api/payroll/bonus
@description Bonus CRUD and list routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.payroll.bonus import BonusService
from core_module.serializers.payroll.bonus import BonusSerializer

bonus_service = BonusService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


def _normalize_fk(data):
    """Normalize FK string IDs to int and map `field` -> `field_id` for Bonus (employee, approved_by)."""
    for fk in ['employee', 'approved_by']:
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
def bonus_list(request):
    if request.method == "GET":
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='id')
        employee = request.GET.get('employee')

        if search:
            from django.db.models import Q
            qs = bonus_service.get_all().filter(
                Q(employee__first_name__icontains=search) |
                Q(employee__last_name__icontains=search) |
                Q(employee__employee_id__icontains=search) |
                Q(bonus_type__icontains=search) |
                Q(status__icontains=search)
            )
            if employee:
                try:
                    qs = qs.filter(employee_id=int(employee))
                except (ValueError, TypeError):
                    pass
        elif employee:
            qs = bonus_service.repository.get_by_employee(employee)
        else:
            qs = bonus_service.get_all()

        allowed_sort = {
            'id': 'id',
            'amount': 'amount',
            'pay_month': 'pay_month',
            'status': 'status',
            'created_at': 'created_at',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='id')
        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)

        return JsonResponse({
            'data': BonusSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })

    data = parse_body(request)
    data = _normalize_fk(data)
    instance, errors = bonus_service.create_bonus(data)

    if instance:
        return JsonResponse(BonusSerializer.serialize(instance), status=201)
        
    return JsonResponse({'errors': errors}, status=400)


@require_login
@safe_json_handler
@require_http_methods(["GET", "PUT", "DELETE"])
def bonus_detail(request, pk):
    if request.method == "GET":
        instance = bonus_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(BonusSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        data = _normalize_fk(data)
        try:
            instance, errors = bonus_service.update(pk, **data)
            if instance:
                return JsonResponse(BonusSerializer.serialize(instance))
            return JsonResponse({'errors': errors}, status=400)
        except Exception as e:
            return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)
    elif request.method == "DELETE":
        success, errors = bonus_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)
