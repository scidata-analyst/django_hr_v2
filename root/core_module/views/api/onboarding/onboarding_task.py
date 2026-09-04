"""
@module views/api/onboarding/onboarding_task
@description Onboarding task CRUD and list routes
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core_module.services.onboarding.onboarding_service import OnboardingTaskService
from core_module.serializers.onboarding_serializers import OnboardingTaskSerializer

onboarding_service = OnboardingTaskService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@csrf_exempt
@require_http_methods(["GET", "POST"])
def onboarding_task_list(request):
    if request.method == "GET":
        employee = request.GET.get('employee')
        status = request.GET.get('status')
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        if search:
            qs = onboarding_service.repository.search_tasks(search)
        elif employee:
            qs = onboarding_service.get_by_employee(employee)
        elif status:
            qs = onboarding_service.repository.get_by_status(status)
        else:
            qs = onboarding_service.get_all()
        
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': OnboardingTaskSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    if 'employee_id' in data and 'create_checklist' in data:
        tasks = onboarding_service.create_onboarding_checklist(data['employee_id'])
        return JsonResponse({'data': OnboardingTaskSerializer.serialize_list(tasks), 'count': len(tasks)}, status=201)
    instance, errors = onboarding_service.create(**data)
    if instance:
        return JsonResponse(OnboardingTaskSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def onboarding_task_detail(request, pk):
    if request.method == "GET":
        instance = onboarding_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(OnboardingTaskSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        instance, errors = onboarding_service.update(pk, **data)
        if instance:
            return JsonResponse(OnboardingTaskSerializer.serialize(instance))
        return JsonResponse({'errors': errors}, status=400)
    elif request.method == "DELETE":
        success, errors = onboarding_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)
