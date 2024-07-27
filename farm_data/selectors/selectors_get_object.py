# farm_data/selector_get_object.py
from typing import List, Any
from django.shortcuts import get_object_or_404
from django.http import Http404

def get_object(model_class: Any, **kwargs: Any) -> Any:
    """
    Attempts to fetch an object based on the provided kwargs.
    If the object does not exist, returns None instead of raising Http404.

    Args:
        model_class (type): The Django model class to query.
        **kwargs: Keyword arguments used to filter the query.

    Returns:
        Any: The queried object if it exists; otherwise, None.
    """
    try:
        return get_object_or_404(model_class, **kwargs)
    except Http404:
        return None