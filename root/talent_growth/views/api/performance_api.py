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
        employee = request.GET.get('employee')
        period = request.GET.get('period')
        status = request.GET.get('status')
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        if search:
            qs = review_service.repository.search_reviews(search)
        elif employee:
            qs = review_service.get_by_employee(employee)
        elif period:
            qs = review_service.repository.get_by_period(period)
        elif status:
            qs = review_service.get_by_status(status)
        else:
            qs = review_service.get_all()

        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': PerformanceReviewSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
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
        employee = request.GET.get('employee')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        if employee:
            qs = goal_service.get_by_employee(employee)
        else:
            qs = goal_service.get_all()

        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': GoalSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
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
