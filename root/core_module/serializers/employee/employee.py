from core_module.models.employee.employee import Employee


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
            'location_id': obj.office_location_id,
            'location_name': obj.office_location.name if obj.office_location else None,
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
        from core_module.serializers.employee.document import DocumentSerializer
        data = EmployeeSerializer.serialize(obj)
        data['documents'] = DocumentSerializer.serialize_list(obj.documents.all())
        data['direct_reports'] = EmployeeSerializer.serialize_list(obj.direct_reports.all())
        return data

    @staticmethod
    def serialize_list(queryset):
        return [EmployeeSerializer.serialize(obj) for obj in queryset]
