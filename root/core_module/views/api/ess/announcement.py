"""
@module views/api/ess/announcement
@description Announcement CRUD and list routes
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core_module.services.ess.ess_service import AnnouncementService
from core_module.serializers.ess_serializers import AnnouncementSerializer

announcement_service = AnnouncementService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@csrf_exempt
@require_http_methods(["GET", "POST"])
def announcement_list(request):
    if request.method == "GET":
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        qs = announcement_service.get_active_announcements()
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': AnnouncementSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    try:
        data = parse_body(request)
        instance, errors = announcement_service.publish(data)
        if instance:
            return JsonResponse(AnnouncementSerializer.serialize(instance), status=201)
        return JsonResponse({'errors': errors}, status=400)
    except Exception as e:
        return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)
