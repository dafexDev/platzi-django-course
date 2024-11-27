from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import get_token


class AddCsrfTokenToContextMiddleware(MiddlewareMixin):
    """
    Add the CSRF token to the context of views that render templates.
    """
    def process_template_response(self, request, response):
        if hasattr(response, 'context_data') and response.context_data is not None:
            response.context_data['csrf_token'] = get_token(request)
        return response
