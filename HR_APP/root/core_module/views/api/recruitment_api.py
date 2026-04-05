import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core_module.services.recruitment.recruitment_service import (
    JobPostingService, CandidateService, InterviewService
)
from core_module.serializers.recruitment_serializers import (
    JobPostingSerializer, CandidateSerializer, InterviewSerializer
)

job_service = JobPostingService()
candidate_service = CandidateService()
interview_service = InterviewService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
@require_http_methods(["GET", "POST"])
def candidate_list(request):
    if request.method == "GET":
        stage = request.GET.get('stage')
        job = request.GET.get('job')
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        if search:
            qs = candidate_service.repository.search_candidates(search)
        elif stage:
            qs = candidate_service.get_by_stage(stage)
        elif job:
            qs = candidate_service.repository.get_by_job(job)
        else:
            qs = candidate_service.get_all()
        
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': CandidateSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    instance, errors = candidate_service.create(**data)
    if instance:
        return JsonResponse(CandidateSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def candidate_detail(request, pk):
    if request.method == "GET":
        instance = candidate_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(CandidateSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        instance, errors = candidate_service.update(pk, **data)
        if instance:
            return JsonResponse(CandidateSerializer.serialize(instance))
        return JsonResponse({'errors': errors}, status=400)
    elif request.method == "DELETE":
        success, errors = candidate_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def candidate_advance(request, pk):
    instance, errors = candidate_service.advance_stage(pk)
    if instance:
        return JsonResponse(CandidateSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def candidate_reject(request, pk):
    instance, errors = candidate_service.reject_candidate(pk)
    if instance:
        return JsonResponse(CandidateSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)


def pipeline_summary(request):
    summary = candidate_service.get_pipeline_summary()
    return JsonResponse({'data': list(summary)})


@csrf_exempt
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


@csrf_exempt
@require_http_methods(["POST"])
def interview_result(request, pk):
    data = parse_body(request)
    instance, errors = interview_service.submit_result(
        pk, data.get('result'), data.get('feedback', ''), data.get('rating')
    )
    if instance:
        return JsonResponse(InterviewSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)