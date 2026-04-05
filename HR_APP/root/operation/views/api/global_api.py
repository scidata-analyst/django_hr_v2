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
        country = request.GET.get('country')
        status = request.GET.get('status')
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        if search:
            qs = office_service.search_offices(search)
        elif country:
            qs = office_service.get_by_country(country)
        elif status:
            qs = office_service.get_by_status(status)
        else:
            qs = office_service.get_all()
        
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': OfficeSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
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
