import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from talent_growth.services.performance.performance_service import (
    PerformanceReviewService, PerformanceKPIService, GoalService
)
from talent_growth.services.training.training_service import (
    TrainingCourseService, CourseEnrollmentService
)
from talent_growth.services.talent.talent_service import (
    TalentProfileService, SuccessionPlanService
)
from talent_growth.services.engagement.engagement_service import (
    EngagementSurveyService, RecognitionService
)
from talent_growth.serializers import (
    PerformanceReviewSerializer, PerformanceKPISerializer, GoalSerializer,
    TrainingCourseSerializer, CourseEnrollmentSerializer,
    TalentProfileSerializer, SuccessionPlanSerializer,
    EngagementSurveySerializer, RecognitionSerializer
)

review_service = PerformanceReviewService()
kpi_service = PerformanceKPIService()
goal_service = GoalService()
course_service = TrainingCourseService()
enrollment_service = CourseEnrollmentService()
talent_service = TalentProfileService()
succession_service = SuccessionPlanService()
survey_service = EngagementSurveyService()
recognition_service = RecognitionService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


# Performance Review APIs
@csrf_exempt
@require_http_methods(["GET", "POST"])
def performance_review_list(request):
    if request.method == "GET":
        employee = request.GET.get('employee')
        period = request.GET.get('period')
        status = request.GET.get('status')
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        if search:
            qs = review_service.repository.search_reviews(search)
        elif employee:
            qs = review_service.get_by_employee(employee)
        elif period:
            qs = review_service.repository.get_by_period(period)
        elif status:
            qs = review_service.get_by_status(status)
        else:
            qs = review_service.get_all()
        
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': PerformanceReviewSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    instance, errors = review_service.create_review(data)
    if instance:
        return JsonResponse(PerformanceReviewSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def performance_review_complete(request, pk):
    data = parse_body(request)
    instance, errors = review_service.complete_review(
        pk, data.get('overall_rating'), data.get('reviewer_comments', '')
    )
    if instance:
        return JsonResponse(PerformanceReviewSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)


# Goal APIs
@csrf_exempt
@require_http_methods(["GET", "POST"])
def goal_list(request):
    if request.method == "GET":
        employee = request.GET.get('employee')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        if employee:
            qs = goal_service.get_by_employee(employee)
        else:
            qs = goal_service.get_all()
        
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': GoalSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    instance, errors = goal_service.create_goal(data)
    if instance:
        return JsonResponse(GoalSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def goal_update_progress(request, pk):
    data = parse_body(request)
    instance, errors = goal_service.update_progress(pk, data.get('progress', 0), data.get('status'))
    if instance:
        return JsonResponse(GoalSerializer.serialize(instance))
    return JsonResponse({'errors': errors}, status=400)


# Training Course APIs
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


# Course Enrollment APIs
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


# Talent Profile APIs
@csrf_exempt
@require_http_methods(["GET", "POST"])
def talent_profile_list(request):
    if request.method == "GET":
        potential = request.GET.get('potential')
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        if search:
            qs = talent_service.repository.search_profiles(search)
        elif potential:
            qs = talent_service.repository.get_by_potential(potential)
        else:
            qs = talent_service.get_all()
        
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': TalentProfileSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    instance, errors = talent_service.create(**data)
    if instance:
        return JsonResponse(TalentProfileSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


# Succession Plan APIs
@csrf_exempt
@require_http_methods(["GET", "POST"])
def succession_plan_list(request):
    if request.method == "GET":
        status = request.GET.get('status')
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        if search:
            qs = succession_service.repository.search_plans(search)
        elif status:
            qs = succession_service.repository.get_by_status(status)
        else:
            qs = succession_service.get_active_plans()
        
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': SuccessionPlanSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    instance, errors = succession_service.create_plan(data)
    if instance:
        return JsonResponse(SuccessionPlanSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


# Survey APIs
@csrf_exempt
@require_http_methods(["GET", "POST"])
def survey_list(request):
    if request.method == "GET":
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        qs = survey_service.get_active_surveys()
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        return JsonResponse({
            'data': EngagementSurveySerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    instance, errors = survey_service.create_survey(data)
    if instance:
        return JsonResponse(EngagementSurveySerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


# Recognition APIs
@csrf_exempt
@require_http_methods(["GET", "POST"])
def recognition_list(request):
    if request.method == "GET":
        employee = request.GET.get('employee')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        if employee:
            qs = recognition_service.get_by_employee(employee)
            total = qs.count()
            start = (page - 1) * page_size
            end = start + page_size
            page_qs = list(qs[start:end])
        else:
            all_qs = list(recognition_service.repository.get_recent(limit=1000))
            total = len(all_qs)
            start = (page - 1) * page_size
            end = start + page_size
            page_qs = all_qs[start:end]
        
        return JsonResponse({
            'data': RecognitionSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
        })
    data = parse_body(request)
    instance, errors = recognition_service.recognize_employee(data)
    if instance:
        return JsonResponse(RecognitionSerializer.serialize(instance), status=201)
    return JsonResponse({'errors': errors}, status=400)


def employee_points(request, employee_id):
    try:
        total = recognition_service.get_total_points(employee_id)
        return JsonResponse({'employee_id': employee_id, 'total_points': total})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)