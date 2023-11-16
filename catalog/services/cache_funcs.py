from typing import Type
from django.conf import settings
from django.core.cache import cache
from django.db.models import Model, QuerySet


def get_all_model_instances_cached(model: Type[Model]) -> QuerySet:
    """
    Takes model, and return cached queryset if exists,
    else takes it from database and set into cache.
    """
    if not hasattr(model, "objects"):
        raise ValueError("Model must be a subclass of the models.Model class.")

    query = model.objects.all

    if settings.CACHE_ENABLED:
        key = f"{model.__name__}_list"
        instances = cache.get_or_set(key, query)
    else:
        instances = query()

    return instances
