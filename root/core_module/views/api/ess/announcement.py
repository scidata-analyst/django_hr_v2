"""
@module views/api/ess/announcement
@description Announcement CRUD and list routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.ess.announcement import AnnouncementService
from core_module.serializers.ess.announcement import AnnouncementSerializer

announcement_service = AnnouncementService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@require_login
@safe_json_handler
@require_http_methods(["GET", "POST"])
def announcement_list(request):
    if request.method == "GET":
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='id')
        qs = announcement_service.get_active_announcements()
        if search:
            from django.db.models import Q
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(priority__icontains=search)
            )
        allowed_sort = {
            'id': 'id',
            'title': 'title',
            'priority': 'priority',
            'created_at': 'created_at',
            'published_at': 'published_at',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='id')
        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)

        return JsonResponse({
            'data': AnnouncementSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })

    try:
        data = parse_body(request)
        instance, errors = announcement_service.publish(data)

        if instance:
            return JsonResponse(AnnouncementSerializer.serialize(instance), status=201)
            
        return JsonResponse({'errors': errors}, status=400)
    except Exception as e:
        return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)
