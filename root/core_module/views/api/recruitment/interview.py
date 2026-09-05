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
from core_module.serializers.recruitment_serializers import InterviewSerializer

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
        candidate = request.GET.get('candidate')

        if candidate:
            qs = interview_service.repository.get_by_candidate(candidate)
        else:
            qs = interview_service.get_all()

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
