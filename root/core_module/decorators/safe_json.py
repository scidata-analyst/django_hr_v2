import logging

from django.http import JsonResponse


def safe_json_handler(view_func):
    logger = logging.getLogger(__name__)

    def _wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as exc:
            logger.exception("API error in %s: %s", view_func.__name__, exc)
            return JsonResponse(
                {'error': 'An internal server error occurred.'},
                status=500,
            )
    return _wrapped_view
