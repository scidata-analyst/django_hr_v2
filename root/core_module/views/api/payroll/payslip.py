"""
@module views/api/payroll/payslip
@description Payslip CRUD, list and bulk generate routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.payroll.payroll_service import PayslipService
from core_module.serializers.payroll_serializers import PayslipSerializer

payslip_service = PayslipService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@require_login
@safe_json_handler
@require_http_methods(["GET", "POST"])
def payslip_list(request):
    if request.method == "GET":
        employee = request.GET.get('employee')
        period = request.GET.get('period')
        month = request.GET.get('month')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        if employee:
            qs = payslip_service.get_by_employee(employee)
        elif period:
            qs = payslip_service.repository.get_by_period(period)
        elif month:
            qs = payslip_service.repository.get_by_period(month)
        else:
            qs = payslip_service.get_all()

        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': PayslipSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    try:
        instance, errors = payslip_service.create(**data)
        if instance:
            return JsonResponse(PayslipSerializer.serialize(instance), status=201)
        return JsonResponse({'errors': errors}, status=400)
    except Exception as e:
        return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)


@require_login
@safe_json_handler
@require_http_methods(["GET"])
def payslip_detail(request, pk):
    instance = payslip_service.get_by_id(pk)
    if instance is None:
        return JsonResponse({'error': 'Not found'}, status=404)
    return JsonResponse(PayslipSerializer.serialize(instance))


@require_login
@safe_json_handler
@require_http_methods(["POST"])
def payslip_bulk_generate(request):
    data = parse_body(request)
    pay_period = data.get('pay_period')
    pay_date = data.get('pay_date')
    if not pay_period or not pay_date:
        return JsonResponse({'error': 'pay_period and pay_date required'}, status=400)
    results = payslip_service.bulk_generate(pay_period, pay_date)
    return JsonResponse(results)
