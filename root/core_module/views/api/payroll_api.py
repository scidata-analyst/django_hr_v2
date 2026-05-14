import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core_module.services.payroll.payroll_service import (
    SalaryStructureService, PayslipService, LoanService, BonusService
)
from core_module.serializers.payroll_serializers import (
    SalaryStructureSerializer, PayslipSerializer, LoanSerializer, BonusSerializer
)

salary_service = SalaryStructureService()
payslip_service = PayslipService()
loan_service = LoanService()
bonus_service = BonusService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@csrf_exempt
@require_http_methods(["GET", "POST"])
def salary_structure_list(request):
    if request.method == "GET":
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        qs = salary_service.get_active()
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
        })
    data = parse_body(request)
    try:
        instance, errors = salary_service.create(**data)
        if instance:
            return JsonResponse(SalaryStructureSerializer.serialize(instance), status=201)
        return JsonResponse({'errors': errors}, status=400)
    except Exception as e:
        return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
@require_http_methods(["GET"])
def payslip_detail(request, pk):
    instance = payslip_service.get_by_id(pk)
    if instance is None:
        return JsonResponse({'error': 'Not found'}, status=404)
    return JsonResponse(PayslipSerializer.serialize(instance))


@csrf_exempt
@require_http_methods(["POST"])
def payslip_bulk_generate(request):
    data = parse_body(request)
    pay_period = data.get('pay_period')
    pay_date = data.get('pay_date')
    if not pay_period or not pay_date:
        return JsonResponse({'error': 'pay_period and pay_date required'}, status=400)
    results = payslip_service.bulk_generate(pay_period, pay_date)
    return JsonResponse(results)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def loan_list(request):
    if request.method == "GET":
        employee = request.GET.get('employee')
        status = request.GET.get('status')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        if employee:
            qs = loan_service.repository.get_by_employee(employee)
        elif status:
            qs = loan_service.repository.get_by_status(status)
        else:
            qs = loan_service.get_all()
        
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': LoanSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    try:
        instance, errors = loan_service.create_loan(data)
        if instance:
            return JsonResponse(LoanSerializer.serialize(instance), status=201)
        return JsonResponse({'errors': errors}, status=400)
    except Exception as e:
        return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def loan_detail(request, pk):
    if request.method == "GET":
        instance = loan_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(LoanSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        try:
            instance, errors = loan_service.update(pk, **data)
            if instance:
                return JsonResponse(LoanSerializer.serialize(instance))
            return JsonResponse({'errors': errors}, status=400)
        except Exception as e:
            return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)
    elif request.method == "DELETE":
        success, errors = loan_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def loan_approve(request, pk):
    data = parse_body(request)
    approved_by_id = data.get('approved_by_id')
    instance, errors = loan_service.approve_loan(pk, approved_by_id)
    if instance:
        return JsonResponse(LoanSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)


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