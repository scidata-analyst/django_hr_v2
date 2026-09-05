"""
@module views/api/payroll/loan
@description Loan CRUD, list and approval routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.payroll.loan import LoanService
from core_module.serializers.payroll.loan import LoanSerializer

loan_service = LoanService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@require_login
@safe_json_handler
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


@require_login
@safe_json_handler
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


@require_login
@safe_json_handler
@require_http_methods(["POST"])
def loan_approve(request, pk):
    data = parse_body(request)
    approved_by_id = data.get('approved_by_id')
    instance, errors = loan_service.approve_loan(pk, approved_by_id)
    if instance:
        return JsonResponse(LoanSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)
