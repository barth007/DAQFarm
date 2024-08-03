#farm_data/middleware.py
from typing import Any
import logging

logger = logging.getLogger(__name__)

class ConditionalCsrfMiddleware:
    """
    Middleware to conditionally bypass CSRF checks based on the request path.

    This middleware allows you to specify a list of URL patterns for which CSRF
    checks will be bypassed. For requests matching any of these URL patterns, the
    middleware sets an attribute on the request object to disable CSRF enforcement.

    Attributes:
        get_response (callable): The next middleware or view in the processing chain.

    Methods:
        __call__(request, *args, **kwargs):
            Processes the request and conditionally disables CSRF checks for specified URLs.

    Usage:
        To use this middleware, add it to the MIDDLEWARE setting in your Django settings module.
        Ensure that this middleware is placed before Django's CsrfViewMiddleware in the list.

    Example:
        MIDDLEWARE = [
            ...
            'path.to.ConditionalCsrfMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            ...
        ]

    Excluded URLs:
        - '/api/'
        - '/soil-data/'
        - '/environ/'
        - '/element-data/'
        - '/hardware/'

    Notes:
        - The `excluded_urls` list contains URL patterns that will bypass CSRF checks.
        - Matching is performed using substring checks, so be cautious about overlapping paths.
    """

    def __init__(self, get_response):
        """
        Initializes the middleware with the get_response callable.

        Args:
            get_response (callable): The next middleware or view in the processing chain.
        """
        self.get_response = get_response

    def __call__(self, request, *args: Any, **kwargs: Any) -> Any:
        """
        Processes the request and sets a flag to bypass CSRF checks for specified URLs.

        Args:
            request (HttpRequest): The incoming request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The response returned by the next middleware or view.
        """
        excluded_urls = [ '/soil-data/', '/environ/', '/element-data/', '/hardware/']
        if any(url in request.path for url in excluded_urls):
            setattr(request, '_dont_enforce_csrf_checks', True)
            logger.debug(f"CSRF check bypassed for URL: {request.path}")
        else:
            logger.debug(f"CSRF check enforced for URL: {request.path}")
        response = self.get_response(request)
        return response

    
       