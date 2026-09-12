"""
@module views/api/onboarding/onboarding_task
@description Onboarding task CRUD and list routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.onboarding.onboarding_task import OnboardingTaskService
from core_module.serializers.onboarding.onboarding_task import OnboardingTaskSerializer

onboarding_service = OnboardingTaskService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@require_login
@safe_json_handler
@require_http_methods(["GET", "POST"])
def onboarding_task_list(request):
    if request.method == "GET":
        employee = request.GET.get('employee')
        status = request.GET.get('status')
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
            'task_name': 'task_name',
            'status': 'status',
            'due_date': 'due_date',
            'created_at': 'created_at',
        }
        sort_field = allowed_sort.get(sort_by, 'id')
        if sort_direction not in ['asc', 'desc']:
            sort_direction = 'desc'
        ordering = sort_field if sort_direction == 'asc' else f'-{sort_field}'

        if search:
            qs = onboarding_service.repository.search_tasks(search)
        elif employee:
            qs = onboarding_service.get_by_employee(employee)
        elif status:
            qs = onboarding_service.repository.get_by_status(status)
        else:
            qs = onboarding_service.get_all()

        if search and employee:
            try:
                qs = qs.filter(employee_id=int(employee))
            except (ValueError, TypeError):
                pass
        if search and status:
            qs = qs.filter(status=status)

        qs = qs.order_by(ordering)

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
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })

    data = parse_body(request)

    if 'employee_id' in data and 'create_checklist' in data:
        tasks = onboarding_service.create_onboarding_checklist(data['employee_id'])
        return JsonResponse({'data': OnboardingTaskSerializer.serialize_list(tasks), 'count': len(tasks)}, status=201)

    instance, errors = onboarding_service.create(**data)

    if instance:
        return JsonResponse(OnboardingTaskSerializer.serialize(instance), status=201)

    return JsonResponse({'errors': errors}, status=400)


@require_login
@safe_json_handler
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
