"""
@module views/api/employee/employee_api
@description Employee CRUD, list and stats routes
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core_module.decorators.permissions import require_login
from core_module.decorators.safe_json import safe_json_handler
from core_module.services.employee.employee import EmployeeService
from core_module.models.employee.employee import Employee
from core_module.serializers.employee.employee import EmployeeSerializer

employee_service = EmployeeService()


def parse_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


def _resolve_fk(data):
    from core_module.models.employee.designation import Designation
    for fk_field in ['department', 'designation', 'reporting_manager', 'office_location']:
        val = data.pop(fk_field, None)
        if val == '' or val is None:
            data[f'{fk_field}_id'] = None
        elif isinstance(val, str) and val.strip():
            val_stripped = val.strip()
            # For designation, allow title string lookup/creation if not numeric
            if fk_field == 'designation' and not val_stripped.isdigit():
                # Try to find designation by title (case-insensitive)
                try:
                    desig = Designation.objects.filter(title__iexact=val_stripped).first()
                    if desig:
                        data[f'{fk_field}_id'] = desig.id
                    else:
                        # Return validation error for unknown designation title - let service handle
                        # Instead of silently dropping, keep error key for frontend
                        data[f'{fk_field}_id'] = None
                        # Store original for error reporting if needed
                        data['_designation_title'] = val_stripped
                    continue
                except Exception:
                    data[f'{fk_field}_id'] = None
                    continue
            try:
                data[f'{fk_field}_id'] = int(val_stripped)
            except (ValueError, TypeError):
                data[f'{fk_field}_id'] = None
        elif isinstance(val, int):
            data[f'{fk_field}_id'] = val
    # If designation title was provided but not found, add error later via service
    if '_designation_title' in data:
        title = data.pop('_designation_title')
        # If designation_id is None and title provided, we could auto-create designation under first department
        # For now, leave as None and let it be blank (designation is optional)
        pass


@require_login
@safe_json_handler
@require_http_methods(["GET", "POST"])
def employee_list(request):
    if request.method == "GET":
        search = request.GET.get('search', '').strip()
        status = request.GET.get('status')
        department = request.GET.get('department')
        sort_by = request.GET.get('sort_by', 'id')
        sort_direction = request.GET.get('sort_direction', 'desc')
        try:
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            if page < 1:
                page = 1
            if page_size < 1:
                page_size = 10
            if page_size > 100:
                page_size = 100
        except (ValueError, TypeError):
            page, page_size = 1, 10

        # Allowed sort fields to prevent injection
        allowed_sort = {
            'id': 'id',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'employee_id': 'employee_id',
            'join_date': 'join_date',
            'created_at': 'created_at',
            'status': 'status',
            'personal_email': 'personal_email',
            'basic_salary': 'basic_salary',
        }
        sort_field = allowed_sort.get(sort_by, 'id')
        if sort_direction not in ['asc', 'desc']:
            sort_direction = 'desc'
        ordering = sort_field if sort_direction == 'asc' else f'-{sort_field}'

        qs = employee_service.get_all()

        if search:
            qs = employee_service.search(search)
        if status:
            qs = qs.filter(status=status)
        if department:
            try:
                qs = qs.filter(department_id=int(department))
            except (ValueError, TypeError):
                pass

        qs = qs.select_related('department', 'designation', 'reporting_manager', 'office_location').order_by(ordering)

        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]

        return JsonResponse({
            'data': EmployeeSerializer.serialize_list(page_qs),
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 1,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
        })

    data = parse_body(request)
    _resolve_fk(data)
    try:
        instance, errors = employee_service.create_employee(data)
        if instance:
            return JsonResponse(EmployeeSerializer.serialize(instance), status=201)
        return JsonResponse({'errors': errors}, status=400)
    except Exception as e:
        return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)


@require_login
@safe_json_handler
@require_http_methods(["GET", "PUT", "DELETE"])
def employee_detail_api(request, pk):
    if request.method == "GET":
        instance = employee_service.get_by_id(pk)
        if instance is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        instance = (
            Employee.objects
            .select_related('department', 'designation', 'reporting_manager', 'office_location')
            .prefetch_related('documents', 'direct_reports')
            .get(pk=pk)
        )
        return JsonResponse(EmployeeSerializer.serialize_detail(instance))

    elif request.method == "PUT":
        data = parse_body(request)
        _resolve_fk(data)
        try:
            instance, errors = employee_service.update_employee(pk, data)
            if instance:
                return JsonResponse(EmployeeSerializer.serialize(instance))
            return JsonResponse({'errors': errors}, status=400)
        except Exception as e:
            return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)

    elif request.method == "DELETE":
        success, errors = employee_service.delete(pk)
        if success:
            return JsonResponse({'message': 'Deleted'}, status=204)
        return JsonResponse({'errors': errors}, status=404)


@require_login
@safe_json_handler
def employee_stats(request):
    stats = employee_service.get_dashboard_stats()
    return JsonResponse(stats)
