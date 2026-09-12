"""
@module views/api/recruitment/candidate
@description Candidate CRUD, pipeline and stage routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.recruitment.candidate import CandidateService
from core_module.serializers.recruitment.candidate import CandidateSerializer

candidate_service = CandidateService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


def _normalize_fk(data):
    """Normalize FK string IDs to int and map `field` -> `field_id` for Candidate (applied_for, hired_employee)."""
    for fk in ['applied_for', 'hired_employee']:
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
def candidate_list(request):
    if request.method == "GET":
        stage = request.GET.get('stage')
        job = request.GET.get('job')
        search = request.GET.get('search', '').strip()
        sort_by = request.GET.get('sort_by', 'id')
        sort_direction = request.GET.get('sort_direction', 'desc')
        try:
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            if page < 1:
                page = 1
            if page_size < 1:
                page_size = 10
            if page_size > 100:
                page_size = 100
        except (ValueError, TypeError):
            page, page_size = 1, 10

        allowed_sort = {
            'id': 'id',
            'full_name': 'full_name',
            'email': 'email',
            'current_stage': 'current_stage',
            'created_at': 'created_at',
            'experience_yrs': 'experience_yrs',
        }
        sort_field = allowed_sort.get(sort_by, 'id')
        if sort_direction not in ['asc', 'desc']:
            sort_direction = 'desc'
        ordering = sort_field if sort_direction == 'asc' else f'-{sort_field}'

        if search:
            qs = candidate_service.repository.search_candidates(search)
        elif stage:
            qs = candidate_service.get_by_stage(stage)
        elif job:
            qs = candidate_service.repository.get_by_job(job)
        else:
            qs = candidate_service.get_all()

        # Apply additional filters when searching
        if search and stage:
            qs = qs.filter(current_stage=stage)
        if search and job:
            try:
                qs = qs.filter(applied_for_id=int(job))
            except (ValueError, TypeError):
                pass

        qs = qs.select_related('applied_for', 'hired_employee').order_by(ordering)

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
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })

    if request.FILES or (request.content_type and 'multipart/form-data' in request.content_type):
        data = request.POST.dict()
        data = _normalize_fk(data)

        if 'resume' in request.FILES:
            data['resume'] = request.FILES['resume']
    else:
        data = parse_body(request)
        data = _normalize_fk(data)

    instance, errors = candidate_service.create(**data)

    if instance:
        return JsonResponse(CandidateSerializer.serialize(instance), status=201)

    return JsonResponse({'errors': errors}, status=400)


@require_login
@safe_json_handler
@require_http_methods(["GET", "PUT", "DELETE"])
def candidate_detail(request, pk):
    if request.method == "GET":
        instance = candidate_service.get_by_id(pk)

        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)

        return JsonResponse(CandidateSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        data = _normalize_fk(data)
        instance, errors = candidate_service.update(pk, **data)

        if instance:
            return JsonResponse(CandidateSerializer.serialize(instance))

        return JsonResponse({'errors': errors}, status=400)
    elif request.method == "DELETE":
        success, errors = candidate_service.delete(pk)

        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)

        return JsonResponse({'errors': errors}, status=404)


@require_login
@safe_json_handler
@require_http_methods(["POST"])
def candidate_advance(request, pk):
    instance, errors = candidate_service.advance_stage(pk)

    if instance:
        return JsonResponse(CandidateSerializer.serialize(instance))

    return JsonResponse({'errors': errors}, status=400)


@require_login
@safe_json_handler
@require_http_methods(["POST"])
def candidate_reject(request, pk):
    instance, errors = candidate_service.reject_candidate(pk)

    if instance:
        return JsonResponse(CandidateSerializer.serialize(instance))
        
    return JsonResponse({'errors': errors}, status=400)


@require_login
@safe_json_handler
def pipeline_summary(request):
    summary = candidate_service.get_pipeline_summary()
    return JsonResponse({'data': list(summary)})
