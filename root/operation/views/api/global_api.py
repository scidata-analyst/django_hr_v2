import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from operation.services.global_ import OfficeService
from operation.serializers.global_ import OfficeSerializer

office_service = OfficeService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@csrf_exempt
@require_http_methods(["GET", "POST"])
def office_list(request):
    if request.method == "GET":
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='name', default_direction='asc')
        country = request.GET.get('country')
        status = request.GET.get('status')

        qs = office_service.get_all()

        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(country__icontains=search) |
                Q(city__icontains=search) |
                Q(office_type__icontains=search) |
                Q(status__icontains=search) |
                Q(full_address__icontains=search)
            )

        if country:
            qs = qs.filter(country__iexact=country)
        if status:
            qs = qs.filter(status=status)

        allowed_sort = {
            'id': 'id',
            'name': 'name',
            'country': 'country',
            'city': 'city',
            'office_type': 'office_type',
            'status': 'status',
            'created_at': 'created_at',
            'capacity': 'capacity',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='name')
        qs = qs.select_related('hr_contact')

        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
        return JsonResponse({
            'data': OfficeSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })
    data = parse_body(request)
    instance, errors = office_service.create(**data)
    if instance:
        return JsonResponse(OfficeSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def office_detail(request, pk):
    if request.method == "GET":
        instance = office_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(OfficeSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        instance, errors = office_service.update(pk, **data)
        if instance:
            return JsonResponse(OfficeSerializer.serialize(instance))
        return JsonResponse({'errors': errors}, status=400)
    elif request.method == "DELETE":
        success, errors = office_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)
