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


def _normalize_fk(data):
    """Normalize FK string IDs to int and map `field` -> `field_id` for ExitInterview (employee, interviewer)."""
    for fk in ['employee', 'interviewer']:
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
    data = _normalize_fk(data)
    instance, errors = exit_service.create(**data)

    if instance:
        return JsonResponse(ExitInterviewSerializer.serialize(instance), status=201)

    return JsonResponse({'errors': errors}, status=400)
