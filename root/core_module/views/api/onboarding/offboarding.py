"""
@module views/api/onboarding/offboarding
@description Offboarding task list and checklist routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.onboarding.onboarding_service import OffboardingTaskService
from core_module.serializers.onboarding_serializers import OffboardingTaskSerializer

offboarding_service = OffboardingTaskService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@require_login
@safe_json_handler
@require_http_methods(["GET", "POST"])
def offboarding_task_list(request):
    if request.method == "GET":
        employee = request.GET.get('employee')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        if employee:
            qs = offboarding_service.repository.get_by_employee(employee)
        else:
            qs = offboarding_service.get_all()

        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': OffboardingTaskSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })

    data = parse_body(request)

    if 'employee_id' in data and 'create_checklist' in data:
        tasks = offboarding_service.create_offboarding_checklist(data['employee_id'])
        return JsonResponse({'data': OffboardingTaskSerializer.serialize_list(tasks), 'count': len(tasks)}, status=201)

    instance, errors = offboarding_service.create(**data)
    
    if instance:
        return JsonResponse(OffboardingTaskSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)
