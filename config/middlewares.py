from django.utils.deprecation import MiddlewareMixin


class DisableCSRFMiddleware(MiddlewareMixin):
    """
    Middleware for disabling CSRF in a specified app name.
    """
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
