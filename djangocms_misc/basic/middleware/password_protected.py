from django.shortcuts import redirect

# compat
import django
if django.VERSION[:2] < (1, 10):
    from django.core.urlresolvers import reverse
else:
    from django.urls import reverse


class PasswordProtectedMiddleware(object):

    def __init__(self, get_response=None):
        if get_response:
            self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        a_possible_redirect = self.process_request(request)
        if a_possible_redirect:
            return a_possible_redirect
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response

    def process_request(self, request):
        # raise a 404 if bot and enabled.
        login_url = reverse('admin:login')
        logout_url = reverse('admin:logout')
        if request.path in (login_url, logout_url,):
            return
        if not request.user.is_authenticated:
            redirect_url = '{}?next={}'.format(login_url, request.path)
            return redirect(redirect_url)
