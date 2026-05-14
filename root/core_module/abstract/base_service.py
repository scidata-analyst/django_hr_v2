from core_module.interface.base_interface import BaseServiceInterface


class BaseService(BaseServiceInterface):
    """
    Base service class for business logic operations.
    All services should inherit from this class.
    """

    def __init__(self, repository=None):
        self.repository = repository

    def process(self, **kwargs):
        pass

    def validate(self, **kwargs):
        return True, {}

    def get_all(self, **filters):
        return self.repository.list(**filters)

    def get_by_id(self, pk):
        return self.repository.read(pk)

    def create(self, **kwargs):
        is_valid, errors = self.validate(**kwargs)
        if not is_valid:
            return None, errors
        try:
            instance = self.repository.create(**kwargs)
            return instance, {}
        except Exception as e:
            return None, {'error': str(e)}

    def update(self, pk, **kwargs):
        try:
            instance = self.repository.update(pk, **kwargs)
            if instance is None:
                return None, {'error': 'Record not found'}
            return instance, {}
        except Exception as e:
            return None, {'error': str(e)}

    def delete(self, pk):
        result = self.repository.delete(pk)
        if not result:
            return False, {'error': 'Record not found'}
        return True, {}
