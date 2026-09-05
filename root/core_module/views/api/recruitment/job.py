"""
@module views/api/recruitment/job
@description Job posting CRUD and list routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.recruitment.job import JobPostingService
from core_module.serializers.recruitment.job import JobPostingSerializer

job_service = JobPostingService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@require_login
@safe_json_handler
@require_http_methods(["GET", "POST"])
def job_posting_list(request):
    if request.method == "GET":
        search = request.GET.get('search', '')
        status = request.GET.get('status')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        if search:
            qs = job_service.search_jobs(search)
        else:
            qs = job_service.get_all()

        if status:
            qs = qs.filter(status=status)

        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]

        return JsonResponse({
            'data': JobPostingSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })

    data = parse_body(request)
    instance, errors = job_service.create(**data)

    if instance:
        return JsonResponse(JobPostingSerializer.serialize(instance), status=201)

    return JsonResponse({'errors': errors}, status=400)


@require_login
@safe_json_handler
@require_http_methods(["GET", "PUT", "DELETE"])
def job_posting_detail(request, pk):
    if request.method == "GET":
        instance = job_service.get_by_id(pk)

        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)

        return JsonResponse(JobPostingSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        instance, errors = job_service.update(pk, **data)

        if instance:
            return JsonResponse(JobPostingSerializer.serialize(instance))

        return JsonResponse({'errors': errors}, status=400)
    elif request.method == "DELETE":
        success, errors = job_service.delete(pk)

        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
            
        return JsonResponse({'errors': errors}, status=404)
