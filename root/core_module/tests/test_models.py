from django.test import TestCase
from django.db.models import Count, Q

from core_module.models.employee.employee import Employee


class AggregationTest(TestCase):
    def test_dashboard_stats_aggregate(self):
        agg = Employee.objects.aggregate(
            total=Count('id'),
            active=Count('id', filter=Q(status='active')),
            probation=Count('id', filter=Q(status='probation')),
            resigned=Count('id', filter=Q(status='resigned')),
            terminated=Count('id', filter=Q(status='terminated')),
        )
        self.assertIn('total', agg)
        self.assertIn('active', agg)
