from core_module.abstract.base_repository import BaseRepository
from operation.models.operation.operation import Report


class ReportRepository(BaseRepository):
    def __init__(self):
        super().__init__(Report)

    def get_by_type(self, report_type):
        return self.model.objects.filter(report_type=report_type)
