"""
@module views/api/payroll/payslip
@description Payslip CRUD, list and bulk generate routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.payroll.payslip import PayslipService
from core_module.serializers.payroll.payslip import PayslipSerializer

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
            'pay_date': 'pay_date',
            'pay_period': 'pay_period',
            'created_at': 'created_at',
            'basic_salary': 'basic_salary',
        }
        sort_field = allowed_sort.get(sort_by, 'id')
        if sort_direction not in ['asc', 'desc']:
            sort_direction = 'desc'
        ordering = sort_field if sort_direction == 'asc' else f'-{sort_field}'

        if search:
            from django.db.models import Q
            qs = payslip_service.get_all().filter(
                Q(employee__first_name__icontains=search) |
                Q(employee__last_name__icontains=search) |
                Q(employee__employee_id__icontains=search) |
                Q(pay_period__icontains=search)
            )
            if employee:
                qs = qs.filter(employee_id=employee)
            if period:
                qs = qs.filter(pay_period__icontains=period)
            if month:
                qs = qs.filter(pay_period__icontains=month)
        elif employee:
            qs = payslip_service.get_by_employee(employee)
        elif period:
            qs = payslip_service.repository.get_by_period(period)
        elif month:
            qs = payslip_service.repository.get_by_period(month)
        else:
            qs = payslip_service.get_all()

        qs = qs.select_related('employee', 'salary_structure').order_by(ordering)

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
            'sort_by': sort_by,
            'sort_direction': sort_direction,
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
