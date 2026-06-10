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
        potential = request.GET.get('potential')
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        if search:
            qs = talent_service.repository.search_profiles(search)
        elif potential:
            qs = talent_service.repository.get_by_potential(potential)
        else:
            qs = talent_service.get_all()

        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': TalentProfileSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
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
        status = request.GET.get('status')
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        if search:
            qs = succession_service.repository.search_plans(search)
        elif status:
            qs = succession_service.repository.get_by_status(status)
        else:
            qs = succession_service.get_active_plans()

        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': SuccessionPlanSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    instance, errors = succession_service.create_plan(data)
    if instance:
        return JsonResponse(SuccessionPlanSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)
