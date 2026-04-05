import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core_module.services.ess.ess_service import ExpenseClaimService, AnnouncementService
from core_module.serializers.ess_serializers import ExpenseClaimSerializer, AnnouncementSerializer

expense_service = ExpenseClaimService()
announcement_service = AnnouncementService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@csrf_exempt
@require_http_methods(["GET", "POST"])
def expense_claim_list(request):
    if request.method == "GET":
        employee = request.GET.get('employee')
        status = request.GET.get('status')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        if employee:
            qs = expense_service.get_by_employee(employee)
        elif status:
            qs = expense_service.repository.get_by_status(status)
        else:
            qs = expense_service.get_all()
        
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': ExpenseClaimSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    try:
        data = parse_body(request)
        instance, errors = expense_service.submit_claim(data)
        if instance:
            return JsonResponse(ExpenseClaimSerializer.serialize(instance), status=201)
        return JsonResponse({'errors': errors}, status=400)
    except Exception as e:
        return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)


@csrf_exempt
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


@csrf_exempt
@require_http_methods(["POST"])
def expense_claim_approve(request, pk):
    data = parse_body(request)
    instance, errors = expense_service.approve_claim(pk, data.get('approved_by_id'))
    if instance:
        return JsonResponse(ExpenseClaimSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def expense_claim_reject(request, pk):
    data = parse_body(request)
    instance, errors = expense_service.reject_claim(
        pk, data.get('approved_by_id'), data.get('rejection_reason', '')
    )
    if instance:
        return JsonResponse(ExpenseClaimSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def announcement_list(request):
    if request.method == "GET":
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        qs = announcement_service.get_active_announcements()
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': AnnouncementSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    try:
        data = parse_body(request)
        instance, errors = announcement_service.publish(data)
        if instance:
            return JsonResponse(AnnouncementSerializer.serialize(instance), status=201)
        return JsonResponse({'errors': errors}, status=400)
    except Exception as e:
        return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)