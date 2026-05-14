from talent_growth.models.talent.talent import TalentProfile, SuccessionPlan


class TalentProfileSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'employee': instance.employee.full_name if instance.employee else None,
            'current_role': instance.current_role,
            'potential': instance.potential,
            'performance_rating': float(instance.performance_rating) if instance.performance_rating else None,
            'readiness': instance.readiness,
            'next_role': instance.next_role,
            'development_areas': instance.development_areas,
            'key_strengths': instance.key_strengths,
            'succession_plan': instance.succession_plan,
        }

    @staticmethod
    def serialize_list(qs):
        return [TalentProfileSerializer.serialize(obj) for obj in qs]


class SuccessionPlanSerializer:
    @staticmethod
    def serialize(instance):
        return {
            'id': instance.id,
            'position': instance.position,
            'department': instance.department.name if instance.department else None,
            'primary_successor': instance.primary_successor.full_name if instance.primary_successor else None,
            'readiness_level': instance.readiness_level,
            'target_date': str(instance.target_date) if instance.target_date else None,
            'is_active': instance.is_active,
        }

    @staticmethod
    def serialize_list(qs):
        return [SuccessionPlanSerializer.serialize(obj) for obj in qs]
