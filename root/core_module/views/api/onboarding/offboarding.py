"""
@module views/api/onboarding/offboarding
@description Offboarding task list and checklist routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.onboarding.offboarding import OffboardingTaskService
from core_module.serializers.onboarding.offboarding import OffboardingTaskSerializer

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
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='due_date', default_direction='desc')
        employee = request.GET.get('employee')
        status = request.GET.get('status')

        if employee:
            qs = offboarding_service.repository.get_by_employee(employee)
        else:
            qs = offboarding_service.get_all()

        if search:
            qs = qs.filter(
                Q(task_name__icontains=search) |
                Q(task_type__icontains=search) |
                Q(description__icontains=search) |
                Q(status__icontains=search) |
                Q(notes__icontains=search) |
                Q(employee__first_name__icontains=search) |
                Q(employee__last_name__icontains=search) |
                Q(employee__employee_id__icontains=search)
            )

        if status:
            qs = qs.filter(status=status)

        allowed_sort = {
            'id': 'id',
            'task_name': 'task_name',
            'task_type': 'task_type',
            'status': 'status',
            'due_date': 'due_date',
            'created_at': 'created_at',
            'completed_date': 'completed_date',
            'employee': 'employee_id',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='due_date')
        qs = qs.select_related('employee', 'assigned_to')

        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
        return JsonResponse({
            'data': OffboardingTaskSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })

    data = parse_body(request)

    if 'employee_id' in data and 'create_checklist' in data:
        tasks = offboarding_service.create_offboarding_checklist(data['employee_id'])
        return JsonResponse({'data': OffboardingTaskSerializer.serialize_list(tasks), 'count': len(tasks)}, status=201)

    instance, errors = offboarding_service.create(**data)
    
    if instance:
        return JsonResponse(OffboardingTaskSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)
