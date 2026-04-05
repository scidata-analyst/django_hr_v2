from operation.models.compliance.compliance import PolicyDocument, PolicyAcknowledgement, ComplianceChecklist


class PolicyDocumentSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'policy_name': instance.policy_name,
            'category': instance.category,
            'version': instance.version,
            'description': instance.description,
            'effective_date': str(instance.effective_date),
            'review_date': str(instance.review_date) if instance.review_date else None,
            'is_mandatory': instance.is_mandatory,
        }

    @staticmethod
    def serialize_list(qs):
        return [PolicyDocumentSerializer.serialize(obj) for obj in qs]


class PolicyAcknowledgementSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'policy': instance.policy.policy_name if instance.policy else None,
            'employee': instance.employee.full_name if instance.employee else None,
            'acknowledged_at': str(instance.acknowledged_at),
        }

    @staticmethod
    def serialize_list(qs):
        return [PolicyAcknowledgementSerializer.serialize(obj) for obj in qs]


class ComplianceChecklistSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'checklist_name': instance.checklist_name,
            'category': instance.category,
            'description': instance.description,
            'due_date': str(instance.due_date) if instance.due_date else None,
            'assigned_to': instance.assigned_to.full_name if instance.assigned_to else None,
            'status': instance.status,
            'notes': instance.notes,
        }

    @staticmethod
    def serialize_list(qs):
        return [ComplianceChecklistSerializer.serialize(obj) for obj in qs]
