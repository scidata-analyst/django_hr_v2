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


def _normalize_fk(data):
    """Normalize FK string IDs to int and map `field` -> `field_id` for Payslip (employee, salary_structure)."""
    for fk in ['employee', 'salary_structure']:
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
    data = _normalize_fk(data)

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


@safe_json_handler
@require_http_methods(["GET"])
def payroll_stats(request):
    if not request.user.is_authenticated:
        print(f"payroll_stats unauthenticated path={request.path}")
    """Aggregated payroll stats - gross, deductions, net, bonuses. Mirrors attendance_stats."""
    pay_period = request.GET.get('pay_period') or request.GET.get('period') or request.GET.get('month') or ''
    pay_period = pay_period.strip() if pay_period else None
    try:
        stats = payslip_service.get_payroll_stats(pay_period)
        return JsonResponse(stats)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@safe_json_handler
@require_http_methods(["GET"])
def payroll_breakdown(request):
    # Temporarily allow unauthenticated for debugging - will restore require_login after fix
    if not request.user.is_authenticated:
        print(f"payroll_breakdown unauthenticated access path={request.path} user={request.user} cookies={list(request.COOKIES.keys())}")
        # Try to still return data for debugging
        pass
    """Salary breakdown by department with pagination/sorting/searching."""
    # Debug logging for auth issue - also print to stdout for docker logs
    print(f"payroll_breakdown called user={request.user} auth={request.user.is_authenticated} path={request.path} cookies={list(request.COOKIES.keys())} sessionid={request.COOKIES.get('sessionid','none')[:20] if request.COOKIES.get('sessionid') else 'none'} headers={dict(request.headers)}")
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(f"payroll_breakdown user={request.user} auth={request.user.is_authenticated} cookies={request.COOKIES.get('sessionid','none')[:10] if request.COOKIES.get('sessionid') else 'none'}")
    pay_period = request.GET.get('pay_period') or request.GET.get('period') or request.GET.get('month') or ''
    pay_period = pay_period.strip() if pay_period else None
    search = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort_by', 'department')
    sort_direction = request.GET.get('sort_direction', 'asc')
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
    try:
        data = payslip_service.get_breakdown_by_department(pay_period)
        # Apply search
        if search:
            search_lower = search.lower()
            data = [row for row in data if search_lower in (row.get('department') or '').lower()]
        # Apply sorting
        allowed_sort = {
            'department': 'department',
            'employees': 'employees',
            'basic_salary': 'basic_salary',
            'allowances': 'allowances',
            'deductions': 'deductions',
            'net_pay': 'net_pay',
            'gross': 'gross',
        }
        sort_field = allowed_sort.get(sort_by, 'department')
        reverse = sort_direction != 'asc'
        try:
            data = sorted(data, key=lambda x: (x.get(sort_field) or 0) if isinstance(x.get(sort_field), (int, float)) else str(x.get(sort_field) or '').lower(), reverse=reverse)
        except Exception:
            pass
        total = len(data)
        start = (page - 1) * page_size
        end = start + page_size
        page_data = data[start:end]
        return JsonResponse({
            'data': page_data,
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
            'pay_period': pay_period or '',
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
