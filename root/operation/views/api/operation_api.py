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
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='plan_name', default_direction='asc')
        status = request.GET.get('status')

        qs = benefit_plan_service.get_all()

        if search:
            qs = qs.filter(
                Q(plan_name__icontains=search) |
                Q(plan_type__icontains=search) |
                Q(coverage_details__icontains=search)
            )

        if status:
            if status == 'active':
                qs = qs.filter(is_active=True)
            elif status == 'inactive':
                qs = qs.filter(is_active=False)
            else:
                qs = qs.filter(is_active=(status.lower() == 'true'))

        allowed_sort = {
            'id': 'id',
            'plan_name': 'plan_name',
            'plan_type': 'plan_type',
            'cost_per_month': 'cost_per_month',
            'created_at': 'created_at',
            'is_active': 'is_active',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='plan_name')

        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
        return JsonResponse({
            'data': BenefitPlanSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
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
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='enrollment_date', default_direction='desc')
        employee = request.GET.get('employee')
        status = request.GET.get('status')

        if employee:
            qs = benefit_enrollment_service.get_by_employee(employee)
        else:
            qs = benefit_enrollment_service.get_all()

        if search:
            qs = qs.filter(
                Q(employee__first_name__icontains=search) |
                Q(employee__last_name__icontains=search) |
                Q(employee__employee_id__icontains=search) |
                Q(plan__plan_name__icontains=search) |
                Q(status__icontains=search)
            )

        if status:
            qs = qs.filter(status=status)

        allowed_sort = {
            'id': 'id',
            'enrollment_date': 'enrollment_date',
            'status': 'status',
            'created_at': 'created_at',
            'coverage_start': 'coverage_start',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='enrollment_date')
        qs = qs.select_related('employee', 'plan')

        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
        return JsonResponse({
            'data': BenefitEnrollmentSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
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
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='incident_date', default_direction='desc')
        status = request.GET.get('status')
        severity = request.GET.get('severity')
        employee = request.GET.get('employee')

        qs = safety_service.get_all() if search or status or severity or employee else safety_service.get_open_incidents()

        if search:
            qs = qs.filter(
                Q(description__icontains=search) |
                Q(location__icontains=search) |
                Q(severity__icontains=search) |
                Q(status__icontains=search) |
                Q(reported_by__first_name__icontains=search) |
                Q(reported_by__last_name__icontains=search)
            )

        if status:
            qs = qs.filter(status=status)
        if severity:
            qs = qs.filter(severity=severity)
        if employee:
            qs = qs.filter(reported_by_id=employee)

        # If no filters and no search, keep open incidents only; otherwise show filtered set
        # To preserve original behavior (open incidents when no filters), we already handled
        # but if search applies, we filter on all; so for non-search case we already used get_open_incidents
        # Ensure sorting
        allowed_sort = {
            'id': 'id',
            'incident_date': 'incident_date',
            'severity': 'severity',
            'status': 'status',
            'created_at': 'created_at',
            'location': 'location',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='incident_date')
        qs = qs.select_related('reported_by', 'assigned_to')

        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
        return JsonResponse({
            'data': SafetyIncidentSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
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
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='effective_date', default_direction='desc')
        category = request.GET.get('category')

        qs = policy_service.get_all()

        if search:
            qs = qs.filter(
                Q(policy_name__icontains=search) |
                Q(category__icontains=search) |
                Q(description__icontains=search)
            )

        if category:
            qs = qs.filter(category=category)

        allowed_sort = {
            'id': 'id',
            'policy_name': 'policy_name',
            'category': 'category',
            'effective_date': 'effective_date',
            'created_at': 'created_at',
            'version': 'version',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='effective_date')
        qs = qs.select_related('created_by')

        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
        return JsonResponse({
            'data': PolicyDocumentSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
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
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='created_at', default_direction='desc')
        status = request.GET.get('status')
        category = request.GET.get('category')

        qs = compliance_service.get_all()

        if search:
            qs = qs.filter(
                Q(checklist_name__icontains=search) |
                Q(category__icontains=search) |
                Q(description__icontains=search) |
                Q(status__icontains=search) |
                Q(notes__icontains=search)
            )

        if status:
            qs = qs.filter(status=status)
        if category:
            qs = qs.filter(category=category)

        allowed_sort = {
            'id': 'id',
            'checklist_name': 'checklist_name',
            'category': 'category',
            'status': 'status',
            'due_date': 'due_date',
            'created_at': 'created_at',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='created_at')
        qs = qs.select_related('assigned_to')

        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
        return JsonResponse({
            'data': ComplianceChecklistSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
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
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='name', default_direction='asc')
        status = request.GET.get('status')
        integration_type = request.GET.get('type') or request.GET.get('integration_type')

        qs = integration_service.get_all()

        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(integration_type__icontains=search) |
                Q(status__icontains=search) |
                Q(webhook_url__icontains=search)
            )

        if status:
            qs = qs.filter(status=status)
        if integration_type:
            qs = qs.filter(integration_type=integration_type)

        allowed_sort = {
            'id': 'id',
            'name': 'name',
            'integration_type': 'integration_type',
            'status': 'status',
            'created_at': 'created_at',
            'is_enabled': 'is_enabled',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='name')

        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
        return JsonResponse({
            'data': IntegrationSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
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
