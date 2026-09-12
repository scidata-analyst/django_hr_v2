"""
@module views/api/employee/document
@description Document CRUD and list routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.employee.document import DocumentService
from core_module.serializers.employee.document import DocumentSerializer

document_service = DocumentService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@require_login
@safe_json_handler
@require_http_methods(["GET", "POST"])
def document_list(request):
    if request.method == "GET":
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search = request.GET.get('search', '').strip()
        sort_by = request.GET.get('sort_by', 'uploaded_at')
        sort_direction = request.GET.get('sort_direction', 'desc')
        has_pagination = 'page' in request.GET or 'page_size' in request.GET

        employee_id = request.GET.get('employee')
        if employee_id:
            qs = document_service.get_by_employee(employee_id)
        else:
            qs = document_service.get_all()

        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(document_type__icontains=search) |
                Q(notes__icontains=search) |
                Q(status__icontains=search) |
                Q(employee__first_name__icontains=search) |
                Q(employee__last_name__icontains=search) |
                Q(employee__employee_id__icontains=search)
            )

        allowed_sort = {
            'id': 'id',
            'title': 'title',
            'document_type': 'document_type',
            'status': 'status',
            'expiry_date': 'expiry_date',
            'uploaded_at': 'uploaded_at',
            'created_at': 'uploaded_at',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='uploaded_at')
        qs = qs.select_related('employee')

        if has_pagination:
            _, _, _, page, page_size = parse_pagination_params(request, default_sort='uploaded_at', default_direction='desc')
            page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
            return JsonResponse({
                'data': DocumentSerializer.serialize_list(page_qs),
                'count': total,
                'page': page,
                'page_size': page_size,
                'total_pages': total_pages,
                'sort_by': sort_by,
                'sort_direction': sort_direction,
            })
        return JsonResponse({'data': DocumentSerializer.serialize_list(qs), 'count': qs.count()})
    if request.FILES or (request.content_type and 'multipart/form-data' in request.content_type):
        data = request.POST.dict()
        if 'file' in request.FILES:
            data['file'] = request.FILES['file']
    else:
        data = parse_body(request)
    instance, errors = document_service.create(**data)
    if instance:
        return JsonResponse(DocumentSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)
