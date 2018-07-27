from django.shortcuts import redirect


class RedirectFirstSubpageMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if getattr(request, 'current_page', None):
            the_page = request.current_page
            the_redirect = the_page.get_redirect()
            # some more checks if in a cms view!
            if view_func.__name__ == 'details' and "slug" in view_kwargs and the_redirect == "/firstchild":
                if getattr(request.current_page, 'get_child_pages', None):
                    subpages = request.current_page.get_child_pages()
                else:
                    subpages = request.current_page.children.all()
                if len(subpages):
                    return redirect(subpages[0].get_absolute_url(), permanent=True)
        return None
