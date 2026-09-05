"""
@module views/api/employee/location
@description Location CRUD and list routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.employee.location import LocationService
from core_module.serializers.employee_serializers import LocationSerializer

location_service = LocationService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@require_login
@safe_json_handler
@require_http_methods(["GET", "POST"])
def location_list(request):
    if request.method == "GET":
        qs = location_service.get_all()
        return JsonResponse({'data': LocationSerializer.serialize_list(qs), 'count': qs.count()})
    data = parse_body(request)
    instance, errors = location_service.create(**data)
    if instance:
        return JsonResponse(LocationSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@require_login
@safe_json_handler
@require_http_methods(["GET", "PUT", "DELETE"])
def location_detail(request, pk):
    if request.method == "GET":
        instance = location_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(LocationSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        instance, errors = location_service.update(pk, **data)
        if instance:
            return JsonResponse(LocationSerializer.serialize(instance))
        return JsonResponse({'errors': errors}, status=400)
    elif request.method == "DELETE":
        success, errors = location_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)
