"""
@module views/api/onboarding/exit_interview
@description Exit interview CRUD and list routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.onboarding.exit_interview import ExitInterviewService
from core_module.serializers.onboarding.exit_interview import ExitInterviewSerializer

exit_service = ExitInterviewService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@require_login
@safe_json_handler
@require_http_methods(["GET", "POST"])
def exit_interview_list(request):
    if request.method == "GET":
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='interview_date', default_direction='desc')
        employee = request.GET.get('employee')

        qs = exit_service.get_all()

        if employee:
            try:
                qs = qs.filter(employee_id=int(employee))
            except (ValueError, TypeError):
                qs = qs.filter(employee_id=employee)

        if search:
            qs = qs.filter(
                Q(reason_for_leaving__icontains=search) |
                Q(feedback__icontains=search) |
                Q(employee__first_name__icontains=search) |
                Q(employee__last_name__icontains=search) |
                Q(employee__employee_id__icontains=search)
            )

        allowed_sort = {
            'id': 'id',
            'interview_date': 'interview_date',
            'rating': 'rating',
            'created_at': 'created_at',
            'employee': 'employee_id',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='interview_date')
        qs = qs.select_related('employee', 'interviewer')

        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
        return JsonResponse({
            'data': ExitInterviewSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })

    data = parse_body(request)
    instance, errors = exit_service.create(**data)

    if instance:
        return JsonResponse(ExitInterviewSerializer.serialize(instance), status=201)

    return JsonResponse({'errors': errors}, status=400)
