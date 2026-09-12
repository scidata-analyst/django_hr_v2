import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from talent_growth.services.training.training_service import (
    TrainingCourseService, CourseEnrollmentService
)
from talent_growth.serializers.training import (
    TrainingCourseSerializer, CourseEnrollmentSerializer
)

course_service = TrainingCourseService()
enrollment_service = CourseEnrollmentService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


@csrf_exempt
@require_http_methods(["GET", "POST"])
def course_list(request):
    if request.method == "GET":
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='course_name', default_direction='asc')
        category = request.GET.get('category')
        status = request.GET.get('status')

        # Preserve original fallback to active when no filters
        if not search and not category and not status:
            qs = course_service.get_active_courses()
        else:
            qs = course_service.get_all()
            if search:
                qs = qs.filter(
                    Q(course_name__icontains=search) |
                    Q(category__icontains=search) |
                    Q(instructor__icontains=search) |
                    Q(description__icontains=search)
                )
            if category:
                qs = qs.filter(category=category)
            if status:
                if status == 'active':
                    qs = qs.filter(is_active=True)
                elif status == 'inactive':
                    qs = qs.filter(is_active=False)

        allowed_sort = {
            'id': 'id',
            'course_name': 'course_name',
            'category': 'category',
            'duration_hours': 'duration_hours',
            'created_at': 'created_at',
            'instructor': 'instructor',
            'is_active': 'is_active',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='course_name')

        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
        return JsonResponse({
            'data': TrainingCourseSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })
    data = parse_body(request)
    instance, errors = course_service.create(**data)
    if instance:
        return JsonResponse(TrainingCourseSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def course_detail(request, pk):
    if request.method == "GET":
        instance = course_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return JsonResponse(TrainingCourseSerializer.serialize(instance))
    elif request.method == "PUT":
        data = parse_body(request)
        instance, errors = course_service.update(pk, **data)
        if instance:
            return JsonResponse(TrainingCourseSerializer.serialize(instance))
        return JsonResponse({'errors': errors}, status=400)
    elif request.method == "DELETE":
        success, errors = course_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def enrollment_list(request):
    if request.method == "GET":
        from core_module.utils.pagination import parse_pagination_params, apply_sorting, paginate_queryset
        from django.db.models import Q

        search, sort_by, sort_direction, page, page_size = parse_pagination_params(request, default_sort='enrollment_date', default_direction='desc')
        employee = request.GET.get('employee')
        course = request.GET.get('course')
        status = request.GET.get('status')

        if employee:
            qs = enrollment_service.get_by_employee(employee)
        elif course:
            qs = enrollment_service.repository.get_by_course(course)
        elif status:
            qs = enrollment_service.repository.get_by_status(status)
        else:
            qs = enrollment_service.get_all()

        if search:
            qs = qs.filter(
                Q(employee__first_name__icontains=search) |
                Q(employee__last_name__icontains=search) |
                Q(employee__employee_id__icontains=search) |
                Q(course__course_name__icontains=search) |
                Q(status__icontains=search) |
                Q(feedback__icontains=search)
            )
            if employee:
                qs = qs.filter(employee_id=employee)
            if course:
                qs = qs.filter(course_id=course)
            if status:
                qs = qs.filter(status=status)
        else:
            # When not searching, still allow combined filters if provided alongside primary filter
            # The above elif chain already handled primary, but if search not provided and multiple params present, ensure all applied
            # For simplicity, if search empty but employee/course/status combo needs AND, we handle via additional checks already done via initial selection
            pass

        # If search was used, we already combined filters; if not, we may need to apply extra filters that were ignored due to elif chain
        # To support combination when search empty but multiple filters provided, re-filter if needed
        if not search:
            # If employee and course both provided, filter further
            # Since qs was selected via elif, check if additional filters present that were not primary
            if employee and course:
                qs = qs.filter(course_id=course)
            if employee and status:
                qs = qs.filter(status=status)
            if course and status and not employee:
                qs = qs.filter(status=status)

        allowed_sort = {
            'id': 'id',
            'enrollment_date': 'enrollment_date',
            'status': 'status',
            'completion_date': 'completion_date',
            'score': 'score',
            'created_at': 'created_at',
        }
        qs = apply_sorting(qs, allowed_sort, sort_by, sort_direction, default='enrollment_date')
        qs = qs.select_related('employee', 'course')

        page_qs, total, total_pages = paginate_queryset(qs, page, page_size)
        return JsonResponse({
            'data': CourseEnrollmentSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })
    data = parse_body(request)
    instance, errors = enrollment_service.enroll_employee(data)
    if instance:
        return JsonResponse(CourseEnrollmentSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def enrollment_complete(request, pk):
    data = parse_body(request)
    instance, errors = enrollment_service.complete_enrollment(
        pk, data.get('score'), data.get('feedback', '')
    )
    if instance:
        return JsonResponse(CourseEnrollmentSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def enrollment_bulk(request):
    data = parse_body(request)
    results = enrollment_service.bulk_enroll(data.get('course_id'), data.get('employee_ids', []))
    return JsonResponse(results)
