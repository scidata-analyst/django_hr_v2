"""
@module views/api/recruitment/interview
@description Interview schedule and result routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.recruitment.interview import InterviewService
from core_module.serializers.recruitment.interview import InterviewSerializer

interview_service = InterviewService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@require_login
@safe_json_handler
@require_http_methods(["GET", "POST"])
def interview_list(request):
    if request.method == "GET":
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search = request.GET.get('search', '').strip()
        sort_by = request.GET.get('sort_by', 'scheduled_at')
        sort_direction = request.GET.get('sort_direction', 'desc')
        has_pagination = 'page' in request.GET or 'page_size' in request.GET

        candidate = request.GET.get('candidate')

        if candidate:
            qs = interview_service.repository.get_by_candidate(candidate)
        else:
            qs = interview_service.get_all()

        if search:
            qs = qs.filter(
                Q(candidate__full_name__icontains=search) |
                Q(candidate__email__icontains=search) |
                Q(interview_type__icontains=search) |
                Q(location__icontains=search) |
                Q(result__icontains=search) |
                Q(feedback__icontains=search)
            )

        allowed_sort = {
            'id': 'id',
            'scheduled_at': 'scheduled_at',
            'interview_type': 'interview_type',
            'result': 'result',
            'rating': 'rating',
            'duration_mins': 'duration_mins',
            'created_at': 'created_at',
            'location': 'location',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='scheduled_at')
        qs = qs.select_related('candidate', 'interviewer')

        if has_pagination:
            _, _, _, page, page_size = parse_pagination_params(request, default_sort='scheduled_at', default_direction='desc')
            # Use already parsed search/sort_by/sort_direction from request (keep consistent with fallback pattern)
            # Re-parse to validate page/page_size via helper, but preserve search/sort from above
            page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
            return JsonResponse({
                'data': InterviewSerializer.serialize_list(page_qs),
                'count': total,
                'page': page,
                'page_size': page_size,
                'total_pages': total_pages,
                'sort_by': sort_by,
                'sort_direction': sort_direction,
            })
        return JsonResponse({'data': InterviewSerializer.serialize_list(qs), 'count': qs.count()})

    data = parse_body(request)
    instance, errors = interview_service.schedule_interview(data)

    if instance:
        return JsonResponse(InterviewSerializer.serialize(instance), status=201)

    return JsonResponse({'errors': errors}, status=400)


@require_login
@safe_json_handler
@require_http_methods(["POST"])
def interview_result(request, pk):
    data = parse_body(request)
    instance, errors = interview_service.submit_result(
        pk, data.get('result'), data.get('feedback', ''), data.get('rating')
    )

    if instance:
        return JsonResponse(InterviewSerializer.serialize(instance))
        
    return JsonResponse({'errors': errors}, status=400)
