from core_module.models.employee.employee import Department, Location, Designation, Employee, Document


class DepartmentSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'description': obj.description,
            'employee_count': obj.employee_set.count(),
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [DepartmentSerializer.serialize(obj) for obj in queryset]


class LocationSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'city': obj.city,
            'country': obj.country,
            'location_type': obj.location_type,
            'location_type_display': obj.get_location_type_display(),
            'is_active': obj.is_active,
            'employee_count': obj.employee_set.count(),
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [LocationSerializer.serialize(obj) for obj in queryset]


class DesignationSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'title': obj.title,
            'department_id': obj.department_id,
            'department_name': obj.department.name if obj.department else None,
            'level': obj.level,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(queryset):
        return [DesignationSerializer.serialize(obj) for obj in queryset]


class EmployeeSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'employee_id': obj.employee_id,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'full_name': obj.full_name,
            'date_of_birth': obj.date_of_birth.isoformat() if obj.date_of_birth else None,
            'gender': obj.gender,
            'gender_display': obj.get_gender_display() if obj.gender else None,
            'national_id': obj.national_id,
            'blood_group': obj.blood_group,
            'personal_email': obj.personal_email,
            'work_email': obj.work_email,
            'phone_number': obj.phone_number,
            'emergency_contact_name': obj.emergency_contact_name,
            'emergency_contact_phone': obj.emergency_contact_phone,
            'current_address': obj.current_address,
            'join_date': obj.join_date.isoformat(),
            'department_id': obj.department_id,
            'department_name': obj.department.name if obj.department else None,
            'designation_id': obj.designation_id,
            'designation_title': obj.designation.title if obj.designation else None,
            'reporting_manager_id': obj.reporting_manager_id,
            'reporting_manager_name': obj.reporting_manager.full_name if obj.reporting_manager else None,
            'office_location_id': obj.office_location_id,
            'office_location_name': obj.office_location.name if obj.office_location else None,
            'employment_type': obj.employment_type,
            'employment_type_display': obj.get_employment_type_display(),
            'status': obj.status,
            'status_display': obj.get_status_display(),
            'basic_salary': str(obj.basic_salary) if obj.basic_salary else None,
            'pay_frequency': obj.pay_frequency,
            'tenure': obj.tenure,
            'resignation_date': obj.resignation_date.isoformat() if obj.resignation_date else None,
            'termination_date': obj.termination_date.isoformat() if obj.termination_date else None,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_detail(obj):
        data = EmployeeSerializer.serialize(obj)
        data['documents'] = DocumentSerializer.serialize_list(obj.documents.all())
        data['direct_reports'] = EmployeeSerializer.serialize_list(obj.direct_reports.all())
        return data

    @staticmethod
    def serialize_list(queryset):
        return [EmployeeSerializer.serialize(obj) for obj in queryset]


class DocumentSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'employee_id': obj.employee_id,
            'employee_name': obj.employee.full_name,
            'document_type': obj.document_type,
            'document_type_display': obj.get_document_type_display(),
            'title': obj.title,
            'file': obj.file.url if obj.file else None,
            'status': obj.status,
            'status_display': obj.get_status_display(),
            'expiry_date': obj.expiry_date.isoformat() if obj.expiry_date else None,
            'notes': obj.notes,
            'uploaded_at': obj.uploaded_at.isoformat(),
            'verified_at': obj.verified_at.isoformat() if obj.verified_at else None,
        }

    @staticmethod
    def serialize_list(queryset):
        return [DocumentSerializer.serialize(obj) for obj in queryset]
