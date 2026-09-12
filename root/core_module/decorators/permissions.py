from functools import wraps

from django.http import JsonResponse


def require_login(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        print(f"require_login check path={request.path} user={request.user} auth={request.user.is_authenticated} cookies={list(request.COOKIES.keys())} sessionid={request.COOKIES.get('sessionid','none')[:20] if request.COOKIES.get('sessionid') else 'none'}")
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"require_login check path={request.path} user={request.user} auth={request.user.is_authenticated}")
        if not request.user.is_authenticated:
            logger.warning(f"require_login failed for {request.path} user={request.user} auth={request.user.is_authenticated} cookies={list(request.COOKIES.keys())} sessionid={request.COOKIES.get('sessionid','none')[:10] if request.COOKIES.get('sessionid') else 'none'} headers={dict(request.headers)}")
            print(f"require_login FAILED for {request.path}")
            return JsonResponse(
                {'error': 'Authentication required.'},
                status=401,
            )
        return view_func(request, *args, **kwargs)
    return _wrapped
