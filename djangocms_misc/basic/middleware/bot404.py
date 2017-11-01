from django.conf import settings
from django.http import Http404


# try to be old and new style middleware compatible
class Bot404Middleware(object):
    def __init__(self, get_response=None):
        if get_response:
            self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        self.process_request(request)
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response

    def process_request(self, request):
        # raise a 404 if bot and enabled.
        enabled = getattr(settings, 'DJANGOCMS_MISC_BOT404', None)
        user_agent = getattr(request, 'user_agent', None)
        if enabled and user_agent and user_agent.is_bot:
            raise Http404
