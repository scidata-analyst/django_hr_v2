"""
@module views/api/ess/expense
@description Expense claim CRUD, approve and reject routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.ess.expense import ExpenseClaimService
from core_module.serializers.ess.expense import ExpenseClaimSerializer

expense_service = ExpenseClaimService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@require_login
@safe_json_handler
@require_http_methods(["GET", "POST"])
def expense_claim_list(request):
    if request.method == "GET":
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='id')
        employee = request.GET.get('employee')
        status = request.GET.get('status')

        if search:
            from django.db.models import Q
            qs = expense_service.get_all().filter(
                Q(employee__first_name__icontains=search) |
                Q(employee__last_name__icontains=search) |
                Q(employee__employee_id__icontains=search) |
                Q(category__icontains=search) |
                Q(status__icontains=search) |
                Q(description__icontains=search)
            )
            if employee:
                try:
                    qs = qs.filter(employee_id=int(employee))
                except (ValueError, TypeError):
                    pass
            if status:
                qs = qs.filter(status=status)
        elif employee:
            qs = expense_service.get_by_employee(employee)
        elif status:
            qs = expense_service.repository.get_by_status(status)
        else:
            qs = expense_service.get_all()

        allowed_sort = {
            'id': 'id',
            'amount': 'amount',
            'expense_date': 'expense_date',
            'status': 'status',
            'created_at': 'created_at',
            'category': 'category',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='id')
        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)

        return JsonResponse({
            'data': ExpenseClaimSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })
    try:
        if request.FILES or (request.content_type and 'multipart/form-data' in request.content_type):
            data = request.POST.dict()

            if 'receipt' in request.FILES:
                data['receipt'] = request.FILES['receipt']
        else:
            data = parse_body(request)

        instance, errors = expense_service.submit_claim(data)

        if instance:
            return JsonResponse(ExpenseClaimSerializer.serialize(instance), status=201)
            
        return JsonResponse({'errors': errors}, status=400)
    except Exception as e:
        return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)


@require_login
@safe_json_handler
@require_http_methods(["GET", "PUT", "DELETE"])
def expense_claim_detail(request, pk):
    if request.method == "GET":
        instance = expense_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(ExpenseClaimSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        instance, errors = expense_service.update(pk, **data)
        if instance:
            return JsonResponse(ExpenseClaimSerializer.serialize(instance))
        return JsonResponse({'errors': errors}, status=400)
    elif request.method == "DELETE":
        success, errors = expense_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)


@require_login
@safe_json_handler
@require_http_methods(["POST"])
def expense_claim_approve(request, pk):
    data = parse_body(request)
    instance, errors = expense_service.approve_claim(pk, data.get('approved_by_id'))
    if instance:
        return JsonResponse(ExpenseClaimSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)


@require_login
@safe_json_handler
@require_http_methods(["POST"])
def expense_claim_reject(request, pk):
    data = parse_body(request)
    instance, errors = expense_service.reject_claim(
        pk, data.get('approved_by_id'), data.get('rejection_reason', '')
    )
    if instance:
        return JsonResponse(ExpenseClaimSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)
