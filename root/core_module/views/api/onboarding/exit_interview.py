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
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        qs = exit_service.get_all()
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        
        return JsonResponse({
            'data': ExitInterviewSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })

    data = parse_body(request)
    instance, errors = exit_service.create(**data)

    if instance:
        return JsonResponse(ExitInterviewSerializer.serialize(instance), status=201)

    return JsonResponse({'errors': errors}, status=400)
