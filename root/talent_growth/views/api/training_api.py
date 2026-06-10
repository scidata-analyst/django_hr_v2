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
        search = request.GET.get('search', '')
        category = request.GET.get('category')
        status = request.GET.get('status')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        if search:
            qs = course_service.repository.search_courses(search)
        elif category:
            qs = course_service.repository.get_by_category(category)
        elif status:
            qs = course_service.repository.get_by_status(status)
        else:
            qs = course_service.get_active_courses()

        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': TrainingCourseSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
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
        employee = request.GET.get('employee')
        course = request.GET.get('course')
        status = request.GET.get('status')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        if employee:
            qs = enrollment_service.get_by_employee(employee)
        elif course:
            qs = enrollment_service.repository.get_by_course(course)
        elif status:
            qs = enrollment_service.repository.get_by_status(status)
        else:
            qs = enrollment_service.get_all()

        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': CourseEnrollmentSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
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
