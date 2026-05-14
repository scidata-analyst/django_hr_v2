from operation.models.operation.operation import (
    BenefitPlan, BenefitEnrollment, SafetyIncident, PolicyDocument,
    PolicyAcknowledgement, ComplianceChecklist, AuditLog, Report, Integration
)


class BenefitPlanSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'plan_name': obj.plan_name,
            'plan_type': obj.plan_type,
            'plan_type_display': obj.get_plan_type_display(),
            'coverage_details': obj.coverage_details,
            'cost_per_month': str(obj.cost_per_month),
            'employer_contribution': str(obj.employer_contribution),
            'is_active': obj.is_active,
            'enrollment_count': obj.enrollments.count(),
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(qs):
        return [BenefitPlanSerializer.serialize(o) for o in qs]


class BenefitEnrollmentSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'employee_id': obj.employee_id,
            'employee_name': obj.employee.full_name,
            'plan_id': obj.plan_id,
            'plan_name': obj.plan.plan_name,
            'enrollment_date': obj.enrollment_date.isoformat(),
            'coverage_start': obj.coverage_start.isoformat(),
            'coverage_end': obj.coverage_end.isoformat() if obj.coverage_end else None,
            'status': obj.status,
            'status_display': obj.get_status_display(),
            'dependent_count': obj.dependent_count,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(qs):
        return [BenefitEnrollmentSerializer.serialize(o) for o in qs]


class SafetyIncidentSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'reported_by_id': obj.reported_by_id,
            'reported_by_name': obj.reported_by.full_name if obj.reported_by else None,
            'incident_date': obj.incident_date.isoformat(),
            'location': obj.location,
            'severity': obj.severity,
            'severity_display': obj.get_severity_display(),
            'description': obj.description,
            'injuries': obj.injuries,
            'witnesses': obj.witnesses,
            'corrective_action': obj.corrective_action,
            'status': obj.status,
            'status_display': obj.get_status_display(),
            'assigned_to_id': obj.assigned_to_id,
            'assigned_to_name': obj.assigned_to.full_name if obj.assigned_to else None,
            'resolved_at': obj.resolved_at.isoformat() if obj.resolved_at else None,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(qs):
        return [SafetyIncidentSerializer.serialize(o) for o in qs]


class PolicyDocumentSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'policy_name': obj.policy_name,
            'category': obj.category,
            'category_display': obj.get_category_display(),
            'version': obj.version,
            'description': obj.description,
            'document_file': obj.document_file.url if obj.document_file else None,
            'effective_date': obj.effective_date.isoformat(),
            'review_date': obj.review_date.isoformat() if obj.review_date else None,
            'is_mandatory': obj.is_mandatory,
            'created_by_id': obj.created_by_id,
            'created_by_name': obj.created_by.full_name if obj.created_by else None,
            'acknowledgement_count': obj.acknowledgements.count(),
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(qs):
        return [PolicyDocumentSerializer.serialize(o) for o in qs]


class ComplianceChecklistSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'checklist_name': obj.checklist_name,
            'category': obj.category,
            'description': obj.description,
            'due_date': obj.due_date.isoformat() if obj.due_date else None,
            'assigned_to_id': obj.assigned_to_id,
            'assigned_to_name': obj.assigned_to.full_name if obj.assigned_to else None,
            'status': obj.status,
            'status_display': obj.get_status_display(),
            'notes': obj.notes,
            'completed_at': obj.completed_at.isoformat() if obj.completed_at else None,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(qs):
        return [ComplianceChecklistSerializer.serialize(o) for o in qs]


class AuditLogSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'user_id': obj.user_id,
            'user_name': obj.user.full_name if obj.user else None,
            'action': obj.action,
            'action_display': obj.get_action_display(),
            'model_name': obj.model_name,
            'object_id': obj.object_id,
            'changes': obj.changes,
            'ip_address': obj.ip_address,
            'timestamp': obj.timestamp.isoformat(),
        }

    @staticmethod
    def serialize_list(qs):
        return [AuditLogSerializer.serialize(o) for o in qs]


class ReportSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'report_name': obj.report_name,
            'report_type': obj.report_type,
            'report_type_display': obj.get_report_type_display(),
            'description': obj.description,
            'parameters': obj.parameters,
            'created_by_id': obj.created_by_id,
            'created_by_name': obj.created_by.full_name if obj.created_by else None,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(qs):
        return [ReportSerializer.serialize(o) for o in qs]


class IntegrationSerializer:
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'integration_type': obj.integration_type,
            'integration_type_display': obj.get_integration_type_display(),
            'webhook_url': obj.webhook_url,
            'is_enabled': obj.is_enabled,
            'status': obj.status,
            'status_display': obj.get_status_display(),
            'last_sync': obj.last_sync.isoformat() if obj.last_sync else None,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_list(qs):
        return [IntegrationSerializer.serialize(o) for o in qs]
