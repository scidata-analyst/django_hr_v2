from operation.interface.base_interface import BaseServiceInterface


class BaseService(BaseServiceInterface):
    """
    Base service class for business logic operations.
    All services should inherit from this class.
    """

    def __init__(self, repository=None):
        """
        Initialize service with repository.
        
        Args:
            repository: Repository instance for data access
        """
        self.repository = repository

    def process(self, **kwargs):
        """
        Process business logic.
        """
        pass

    def validate(self, **kwargs):
        """
        Validate input data.
        
        Returns:
            tuple: (is_valid: bool, errors: dict)
        """
        pass
