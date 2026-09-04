"""
@module views/api/payroll/bonus
@description Bonus CRUD and list routes
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core_module.services.payroll.payroll_service import BonusService
from core_module.serializers.payroll_serializers import BonusSerializer

bonus_service = BonusService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@csrf_exempt
@require_http_methods(["GET", "POST"])
def bonus_list(request):
    if request.method == "GET":
        employee = request.GET.get('employee')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        if employee:
            qs = bonus_service.repository.get_by_employee(employee)
        else:
            qs = bonus_service.get_all()
        
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': BonusSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    instance, errors = bonus_service.create_bonus(data)
    if instance:
        return JsonResponse(BonusSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)
