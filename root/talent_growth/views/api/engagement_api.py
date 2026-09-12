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


def _normalize_fk(data, fields=None):
    if fields is None:
        fields = ['employee', 'recognized_by']
    for fk in fields:
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


@csrf_exempt
@require_http_methods(["GET", "POST"])
def survey_list(request):
    if request.method == "GET":
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='start_date', default_direction='desc')
        is_active = request.GET.get('is_active')

        qs = survey_service.get_all() if search else survey_service.get_active_surveys()

        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        if is_active is not None:
            if is_active.lower() in ['true', '1']:
                qs = qs.filter(is_active=True)
            elif is_active.lower() in ['false', '0']:
                qs = qs.filter(is_active=False)

        allowed_sort = {
            'id': 'id',
            'title': 'title',
            'start_date': 'start_date',
            'end_date': 'end_date',
            'created_at': 'created_at',
            'is_active': 'is_active',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='start_date')

        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
        return JsonResponse({
            'data': EngagementSurveySerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
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
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='given_at', default_direction='desc')
        employee = request.GET.get('employee')

        if employee:
            qs = recognition_service.get_by_employee(employee)
        else:
            # Use get_all for full queryset to allow sorting/filtering correctly
            qs = recognition_service.get_all()

        if search:
            qs = qs.filter(
                Q(reason__icontains=search) |
                Q(recognition_type__icontains=search) |
                Q(employee__first_name__icontains=search) |
                Q(employee__last_name__icontains=search) |
                Q(employee__employee_id__icontains=search) |
                Q(recognized_by__first_name__icontains=search) |
                Q(recognized_by__last_name__icontains=search)
            )

        allowed_sort = {
            'id': 'id',
            'recognition_type': 'recognition_type',
            'points': 'points',
            'given_at': 'given_at',
            'created_at': 'given_at',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='given_at')
        qs = qs.select_related('employee', 'recognized_by')

        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
        return JsonResponse({
            'data': RecognitionSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })
    data = parse_body(request)
    data = _normalize_fk(data, ['employee', 'recognized_by'])
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
