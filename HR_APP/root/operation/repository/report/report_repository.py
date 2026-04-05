from operation.abstract.base_repository import BaseRepository


class ReportRepository(BaseRepository):
    """
    Repository for reporting data access operations.
    """

    def create(self, **kwargs):
        """
        Create a new report record in the database.
        """
        pass

    def read(self, pk):
        """
        Read a report record from the database by primary key.
        """
        pass

    def update(self, pk, **kwargs):
        """
        Update an existing report record in the database.
        """
        pass

    def delete(self, pk):
        """
        Delete a report record from the database.
        """
        pass

    def list(self, **filters):
        """
        List report records based on filters.
        """
        pass
