from operation.models.health.health import BenefitPlan, BenefitEnrollment, SafetyIncident


class BenefitPlanSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'plan_name': instance.plan_name,
            'plan_type': instance.plan_type,
            'coverage_details': instance.coverage_details,
            'cost_per_month': float(instance.cost_per_month),
            'employer_contribution': float(instance.employer_contribution),
            'is_active': instance.is_active,
        }

    @staticmethod
    def serialize_list(qs):
        return [BenefitPlanSerializer.serialize(obj) for obj in qs]


class BenefitEnrollmentSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'employee': instance.employee.full_name if instance.employee else None,
            'plan': instance.plan.plan_name if instance.plan else None,
            'enrollment_date': str(instance.enrollment_date),
            'coverage_start': str(instance.coverage_start),
            'coverage_end': str(instance.coverage_end) if instance.coverage_end else None,
            'status': instance.status,
            'dependent_count': instance.dependent_count,
        }

    @staticmethod
    def serialize_list(qs):
        return [BenefitEnrollmentSerializer.serialize(obj) for obj in qs]


class SafetyIncidentSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'reported_by': instance.reported_by.full_name if instance.reported_by else None,
            'incident_date': str(instance.incident_date),
            'location': instance.location,
            'severity': instance.severity,
            'description': instance.description,
            'injuries': instance.injuries,
            'witnesses': instance.witnesses,
            'corrective_action': instance.corrective_action,
            'status': instance.status,
            'assigned_to': instance.assigned_to.full_name if instance.assigned_to else None,
        }

    @staticmethod
    def serialize_list(qs):
        return [SafetyIncidentSerializer.serialize(obj) for obj in qs]
