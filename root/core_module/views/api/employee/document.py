import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core_module.services.employee.employee_service import DocumentService
from core_module.serializers.employee_serializers import DocumentSerializer

document_service = DocumentService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@csrf_exempt
@require_http_methods(["GET", "POST"])
def document_list(request):
    if request.method == "GET":
        employee_id = request.GET.get('employee')
        if employee_id:
            qs = document_service.get_by_employee(employee_id)
        else:
            qs = document_service.get_all()
        return JsonResponse({'data': DocumentSerializer.serialize_list(qs), 'count': qs.count()})
    data = parse_body(request)
    instance, errors = document_service.create(**data)
    if instance:
        return JsonResponse(DocumentSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)
