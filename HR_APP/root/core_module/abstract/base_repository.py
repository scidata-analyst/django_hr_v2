from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from core_module.interface.base_interface import BaseRepositoryInterface


class BaseRepository(BaseRepositoryInterface):
    """
    Base repository class with common CRUD operations.
    All repositories should inherit from this class.
    """

    def __init__(self, model: models.Model):
        self.model = model

    def create(self, **kwargs):
        instance = self.model(**kwargs)
        try:
            instance.full_clean()
        except ValidationError as e:
            raise e
        instance.save()
        return instance

    def read(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return None

    def update(self, pk, **kwargs):
        instance = self.read(pk)
        if instance is None:
            return None
        for key, value in kwargs.items():
            setattr(instance, key, value)
        try:
            instance.full_clean()
        except ValidationError as e:
            raise e
        instance.save()
        return instance

    def delete(self, pk):
        instance = self.read(pk)
        if instance is None:
            return False
        instance.delete()
        return True

    def list(self, **filters):
        queryset = self.model.objects.all()
        if filters:
            queryset = queryset.filter(**filters)
        return queryset

    def search(self, search_fields, query):
        if not query:
            return self.model.objects.all()
        q_objects = Q()
        for field in search_fields:
            q_objects |= Q(**{f"{field}__icontains": query})
        return self.model.objects.filter(q_objects)

    def count(self, **filters):
        return self.model.objects.filter(**filters).count()

    def exists(self, pk):
        return self.model.objects.filter(pk=pk).exists()
