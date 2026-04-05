from django.db import models
from talent_growth.interface.base_interface import BaseRepositoryInterface


class BaseRepository(BaseRepositoryInterface):
    """
    Base repository class with common CRUD operations.
    All repositories should inherit from this class.
    """

    def __init__(self, model: models.Model):
        """
        Initialize repository with a model.
        
        Args:
            model: Django model class
        """
        self.model = model

    def create(self, **kwargs):
        """
        Create a new record in the database.
        """
        pass

    def read(self, pk):
        """
        Read a record from the database by primary key.
        """
        pass

    def update(self, pk, **kwargs):
        """
        Update an existing record in the database.
        """
        pass

    def delete(self, pk):
        """
        Delete a record from the database.
        """
        pass

    def list(self, **filters):
        """
        List records based on filters.
        """
        pass
