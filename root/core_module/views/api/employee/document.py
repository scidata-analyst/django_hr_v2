"""
@module views/api/employee/document
@description Document CRUD and list routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.employee.employee_service import DocumentService
from core_module.serializers.employee_serializers import DocumentSerializer

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
        employee_id = request.GET.get('employee')
        if employee_id:
            qs = document_service.get_by_employee(employee_id)
        else:
            qs = document_service.get_all()
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
