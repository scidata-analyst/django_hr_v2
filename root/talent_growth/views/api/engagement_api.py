import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from talent_growth.services.engagement.engagement_service import (
    EngagementSurveyService, RecognitionService
)
from talent_growth.serializers.engagement import (
    EngagementSurveySerializer, RecognitionSerializer
)

survey_service = EngagementSurveyService()
recognition_service = RecognitionService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@csrf_exempt
@require_http_methods(["GET", "POST"])
def survey_list(request):
    if request.method == "GET":
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        qs = survey_service.get_active_surveys()
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': EngagementSurveySerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    instance, errors = survey_service.create_survey(data)
    if instance:
        return JsonResponse(EngagementSurveySerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def recognition_list(request):
    if request.method == "GET":
        employee = request.GET.get('employee')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        if employee:
            qs = recognition_service.get_by_employee(employee)
            total = qs.count()
            start = (page - 1) * page_size
            end = start + page_size
            page_qs = list(qs[start:end])
        else:
            all_qs = list(recognition_service.get_recent(limit=1000))
            total = len(all_qs)
            start = (page - 1) * page_size
            end = start + page_size
            page_qs = all_qs[start:end]

        return JsonResponse({
            'data': RecognitionSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    instance, errors = recognition_service.recognize_employee(data)
    if instance:
        return JsonResponse(RecognitionSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


def employee_points(request, employee_id):
    try:
        total = recognition_service.get_total_points(employee_id)
        return JsonResponse({'employee_id': employee_id, 'total_points': total})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
