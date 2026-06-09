import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from operation.services.benefit_service import BenefitPlanService, BenefitEnrollmentService
from operation.services.safety_service import SafetyIncidentService
from operation.services.compliance_service import (
    PolicyDocumentService, PolicyAcknowledgementService, ComplianceChecklistService
)
from operation.services.report_service import ReportService
from operation.services.integration_service import IntegrationService
from operation.serializers import (
    BenefitPlanSerializer, BenefitEnrollmentSerializer, SafetyIncidentSerializer,
    PolicyDocumentSerializer, ComplianceChecklistSerializer, IntegrationSerializer
)

benefit_plan_service = BenefitPlanService()
benefit_enrollment_service = BenefitEnrollmentService()
safety_service = SafetyIncidentService()
policy_service = PolicyDocumentService()
ack_service = PolicyAcknowledgementService()
compliance_service = ComplianceChecklistService()
report_service = ReportService()
integration_service = IntegrationService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


# Benefit Plan APIs
@csrf_exempt
@require_http_methods(["GET", "POST"])
def benefit_plan_list(request):
    if request.method == "GET":
        search = request.GET.get('search', '')
        status = request.GET.get('status')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        if search:
            qs = benefit_plan_service.repository.search_plans(search)
        elif status:
            qs = benefit_plan_service.repository.get_by_status(status)
        else:
            qs = benefit_plan_service.get_all()
        
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': BenefitPlanSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    instance, errors = benefit_plan_service.create(**data)
    if instance:
        return JsonResponse(BenefitPlanSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def benefit_plan_detail(request, pk):
    if request.method == "GET":
        instance = benefit_plan_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(BenefitPlanSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        instance, errors = benefit_plan_service.update(pk, **data)
        if instance:
            return JsonResponse(BenefitPlanSerializer.serialize(instance))
        return JsonResponse({'errors': errors}, status=400)
    elif request.method == "DELETE":
        success, errors = benefit_plan_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)


# Benefit Enrollment APIs
@csrf_exempt
@require_http_methods(["GET", "POST"])
def benefit_enrollment_list(request):
    if request.method == "GET":
        employee = request.GET.get('employee')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        if employee:
            qs = benefit_enrollment_service.get_by_employee(employee)
        else:
            qs = benefit_enrollment_service.get_all()
        
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': BenefitEnrollmentSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    instance, errors = benefit_enrollment_service.enroll(data)
    if instance:
        return JsonResponse(BenefitEnrollmentSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


# Safety Incident APIs
@csrf_exempt
@require_http_methods(["GET", "POST"])
def safety_incident_list(request):
    if request.method == "GET":
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        qs = safety_service.get_open_incidents()
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': SafetyIncidentSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    instance, errors = safety_service.report_incident(data)
    if instance:
        return JsonResponse(SafetyIncidentSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def safety_incident_resolve(request, pk):
    data = parse_body(request)
    instance, errors = safety_service.resolve_incident(pk, data.get('corrective_action', ''))
    if instance:
        return JsonResponse(SafetyIncidentSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)


# Policy APIs
@csrf_exempt
@require_http_methods(["GET", "POST"])
def policy_list(request):
    if request.method == "GET":
        search = request.GET.get('search', '')
        category = request.GET.get('category')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        if search:
            qs = policy_service.repository.search_policies(search)
        elif category:
            qs = policy_service.repository.get_by_category(category)
        else:
            qs = policy_service.get_all()
        
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': PolicyDocumentSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    instance, errors = policy_service.create(**data)
    if instance:
        return JsonResponse(PolicyDocumentSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def policy_detail(request, pk):
    if request.method == "GET":
        instance = policy_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(PolicyDocumentSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        instance, errors = policy_service.update(pk, **data)
        if instance:
            return JsonResponse(PolicyDocumentSerializer.serialize(instance))
        return JsonResponse({'errors': errors}, status=400)
    elif request.method == "DELETE":
        success, errors = policy_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def policy_acknowledge(request, pk):
    data = parse_body(request)
    instance, meta = ack_service.acknowledge_policy(pk, data.get('employee_id'))
    return JsonResponse({'acknowledged': True, 'is_new': meta.get('is_new')})


# Compliance Checklist APIs
@csrf_exempt
@require_http_methods(["GET", "POST"])
def compliance_list(request):
    if request.method == "GET":
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        qs = compliance_service.get_all()
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': ComplianceChecklistSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    instance, errors = compliance_service.create(**data)
    if instance:
        return JsonResponse(ComplianceChecklistSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def compliance_complete(request, pk):
    data = parse_body(request)
    instance, errors = compliance_service.complete_item(pk, data.get('notes', ''))
    if instance:
        return JsonResponse(ComplianceChecklistSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)


# Report APIs
def report_headcount(request):
    try:
        data = report_service.generate_headcount_report()
        return JsonResponse({'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def report_attendance(request):
    try:
        start = request.GET.get('start_date') or '2000-01-01'
        end = request.GET.get('end_date') or '2099-12-31'
        data = report_service.generate_attendance_report(start, end)
        return JsonResponse({'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def report_turnover(request):
    try:
        data = report_service.generate_turnover_report()
        return JsonResponse({'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Integration APIs
@csrf_exempt
@require_http_methods(["GET", "POST"])
def integration_list(request):
    if request.method == "GET":
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        qs = integration_service.get_all()
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': IntegrationSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    instance, errors = integration_service.create(**data)
    if instance:
        return JsonResponse(IntegrationSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def integration_toggle(request, pk):
    instance, errors = integration_service.toggle_integration(pk)
    if instance:
        return JsonResponse(IntegrationSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=404)