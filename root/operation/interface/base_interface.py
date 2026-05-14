from abc import ABC, abstractmethod


class BaseRepositoryInterface(ABC):
    """
    Base interface for repository layer.
    All repositories should inherit from this interface.
    """

    @abstractmethod
    def create(self, **kwargs):
        """
        Create a new record in the database.
        """
        pass

    @abstractmethod
    def read(self, pk):
        """
        Read a record from the database by primary key.
        """
        pass

    @abstractmethod
    def update(self, pk, **kwargs):
        """
        Update an existing record in the database.
        """
        pass

    @abstractmethod
    def delete(self, pk):
        """
        Delete a record from the database.
        """
        pass

    @abstractmethod
    def list(self, **filters):
        """
        List records based on filters.
        """
        pass


class BaseServiceInterface(ABC):
    """
    Base interface for service layer.
    All services should inherit from this interface.
    """

    @abstractmethod
    def process(self, **kwargs):
        """
        Process business logic.
        """
        pass

    @abstractmethod
    def validate(self, **kwargs):
        """
        Validate input data.
        """
        pass
