import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from talent_growth.services.talent.talent_service import (
    TalentProfileService, SuccessionPlanService
)
from talent_growth.serializers.talent import (
    TalentProfileSerializer, SuccessionPlanSerializer
)

talent_service = TalentProfileService()
succession_service = SuccessionPlanService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@csrf_exempt
@require_http_methods(["GET", "POST"])
def talent_profile_list(request):
    if request.method == "GET":
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='created_at', default_direction='desc')
        potential = request.GET.get('potential')
        readiness = request.GET.get('readiness')

        qs = talent_service.get_all()

        if search:
            qs = qs.filter(
                Q(employee__first_name__icontains=search) |
                Q(employee__last_name__icontains=search) |
                Q(employee__employee_id__icontains=search) |
                Q(current_role__icontains=search) |
                Q(next_role__icontains=search) |
                Q(development_areas__icontains=search) |
                Q(key_strengths__icontains=search) |
                Q(potential__icontains=search)
            )

        if potential:
            qs = qs.filter(potential=potential)
        if readiness:
            qs = qs.filter(readiness=readiness)

        allowed_sort = {
            'id': 'id',
            'current_role': 'current_role',
            'potential': 'potential',
            'readiness': 'readiness',
            'created_at': 'created_at',
            'performance_rating': 'performance_rating',
            'next_role': 'next_role',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='created_at')
        qs = qs.select_related('employee')

        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
        return JsonResponse({
            'data': TalentProfileSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })
    data = parse_body(request)
    instance, errors = talent_service.create(**data)
    if instance:
        return JsonResponse(TalentProfileSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def succession_plan_list(request):
    if request.method == "GET":
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='created_at', default_direction='desc')
        status = request.GET.get('status')
        department = request.GET.get('department')
        is_active = request.GET.get('is_active')

        # Preserve original fallback to active when no filters
        if not search and not status and not department and is_active is None:
            qs = succession_service.get_active_plans()
        else:
            qs = succession_service.get_all()
            if search:
                qs = qs.filter(
                    Q(position__icontains=search) |
                    Q(department__name__icontains=search) |
                    Q(primary_successor__first_name__icontains=search) |
                    Q(primary_successor__last_name__icontains=search) |
                    Q(readiness_level__icontains=search)
                )
            if status:
                if status in ['active', 'inactive']:
                    is_active_val = status == 'active'
                    qs = qs.filter(is_active=is_active_val)
                else:
                    qs = qs.filter(readiness_level=status)
            if department:
                qs = qs.filter(department_id=department)
            if is_active is not None:
                if is_active.lower() in ['true', '1']:
                    qs = qs.filter(is_active=True)
                elif is_active.lower() in ['false', '0']:
                    qs = qs.filter(is_active=False)

        allowed_sort = {
            'id': 'id',
            'position': 'position',
            'readiness_level': 'readiness_level',
            'target_date': 'target_date',
            'created_at': 'created_at',
            'is_active': 'is_active',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='created_at')
        qs = qs.select_related('department', 'primary_successor')

        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
        return JsonResponse({
            'data': SuccessionPlanSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })
    data = parse_body(request)
    instance, errors = succession_service.create_plan(data)
    if instance:
        return JsonResponse(SuccessionPlanSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)
