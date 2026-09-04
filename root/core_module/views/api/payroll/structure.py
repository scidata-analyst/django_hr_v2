import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core_module.services.payroll.payroll_service import SalaryStructureService
from core_module.serializers.payroll_serializers import SalaryStructureSerializer

salary_service = SalaryStructureService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@csrf_exempt
@require_http_methods(["GET", "POST"])
def salary_structure_list(request):
    if request.method == "GET":
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        qs = salary_service.get_active()
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': SalaryStructureSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    try:
        instance, errors = salary_service.create(**data)
        if instance:
            return JsonResponse(SalaryStructureSerializer.serialize(instance), status=201)
        return JsonResponse({'errors': errors}, status=400)
    except Exception as e:
        return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def salary_structure_detail(request, pk):
    if request.method == "GET":
        instance = salary_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(SalaryStructureSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        try:
            instance, errors = salary_service.update(pk, **data)
            if instance:
                return JsonResponse(SalaryStructureSerializer.serialize(instance))
            return JsonResponse({'errors': errors}, status=400)
        except Exception as e:
            return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)
    elif request.method == "DELETE":
        success, errors = salary_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)
