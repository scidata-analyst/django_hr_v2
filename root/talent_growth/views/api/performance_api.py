import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from talent_growth.services.performance.performance_service import (
    PerformanceReviewService, GoalService
)
from talent_growth.serializers.performance import (
    PerformanceReviewSerializer, GoalSerializer
)

review_service = PerformanceReviewService()
goal_service = GoalService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@csrf_exempt
@require_http_methods(["GET", "POST"])
def performance_review_list(request):
    if request.method == "GET":
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='created_at', default_direction='desc')
        employee = request.GET.get('employee')
        period = request.GET.get('period')
        status = request.GET.get('status')

        qs = review_service.get_all()

        if search:
            qs = qs.filter(
                Q(employee__first_name__icontains=search) |
                Q(employee__last_name__icontains=search) |
                Q(employee__employee_id__icontains=search) |
                Q(review_period__icontains=search) |
                Q(department__name__icontains=search) |
                Q(status__icontains=search) |
                Q(reviewer_comments__icontains=search)
            )

        if employee:
            qs = qs.filter(employee_id=employee)
        if period:
            qs = qs.filter(review_period=period)
        if status:
            qs = qs.filter(status=status)

        allowed_sort = {
            'id': 'id',
            'review_period': 'review_period',
            'start_date': 'start_date',
            'end_date': 'end_date',
            'overall_rating': 'overall_rating',
            'status': 'status',
            'created_at': 'created_at',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='created_at')
        qs = qs.select_related('employee', 'department', 'reviewer')

        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
        return JsonResponse({
            'data': PerformanceReviewSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })
    data = parse_body(request)
    instance, errors = review_service.create_review(data)
    if instance:
        return JsonResponse(PerformanceReviewSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def performance_review_complete(request, pk):
    data = parse_body(request)
    instance, errors = review_service.complete_review(
        pk, data.get('overall_rating'), data.get('reviewer_comments', '')
    )
    if instance:
        return JsonResponse(PerformanceReviewSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def goal_list(request):
    if request.method == "GET":
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='created_at', default_direction='desc')
        employee = request.GET.get('employee')
        status = request.GET.get('status')

        if employee:
            qs = goal_service.get_by_employee(employee)
        else:
            qs = goal_service.get_all()

        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(status__icontains=search) |
                Q(employee__first_name__icontains=search) |
                Q(employee__last_name__icontains=search)
            )

        if status:
            qs = qs.filter(status=status)

        allowed_sort = {
            'id': 'id',
            'title': 'title',
            'status': 'status',
            'due_date': 'due_date',
            'progress': 'progress',
            'created_at': 'created_at',
            'start_date': 'start_date',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='created_at')
        qs = qs.select_related('employee')

        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
        return JsonResponse({
            'data': GoalSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })
    data = parse_body(request)
    instance, errors = goal_service.create_goal(data)
    if instance:
        return JsonResponse(GoalSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def goal_update_progress(request, pk):
    data = parse_body(request)
    instance, errors = goal_service.update_progress(pk, data.get('progress', 0), data.get('status'))
    if instance:
        return JsonResponse(GoalSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)
