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
    instance, errors = bonus_service.create_bonus(data)

    if instance:
        return JsonResponse(BonusSerializer.serialize(instance), status=201)
        
    return JsonResponse({'errors': errors}, status=400)
