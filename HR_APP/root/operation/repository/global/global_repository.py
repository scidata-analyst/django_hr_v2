from operation.abstract.base_repository import BaseRepository


class GlobalRepository(BaseRepository):
    """
    Repository for global operations data access operations.
    """

    def create(self, **kwargs):
        """
        Create a new global operations record in the database.
        """
        pass

    def read(self, pk):
        """
        Read a global operations record from the database by primary key.
        """
        pass

    def update(self, pk, **kwargs):
        """
        Update an existing global operations record in the database.
        """
        pass

    def delete(self, pk):
        """
        Delete a global operations record from the database.
        """
        pass

    def list(self, **filters):
        """
        List global operations records based on filters.
        """
        pass
