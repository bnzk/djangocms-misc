
from cms.plugin_rendering import ContentRenderer, RenderedPlaceholder


def content_renderer__init__(self, request):
    self.__old_init__(request)
    self.request_language = 'en'


ContentRenderer.__old_init__ = ContentRenderer.__init__
ContentRenderer.__init__ = content_renderer__init__


def render_placeholder(self, placeholder, context, language=None, page=None,
                       editable=False, use_cache=False, nodelist=None, width=None):
    language = 'en'
    self.__old_render_placeholder(placeholder, context, language, page,
                       editable, use_cache, nodelist, width)


ContentRenderer.__old_render_placeholder = ContentRenderer.render_placeholder
ContentRenderer.render_placeholder = render_placeholder


def rendered_placeholder__init__(self, placeholder, language, site_id, cached=False,
                 editable=False, has_content=False):
    language = 'en'
    self.__old_init__(placeholder, language, site_id, cached, editable, has_content)


RenderedPlaceholder.__old_init__ = RenderedPlaceholder.__init__
RenderedPlaceholder.__init__ = rendered_placeholder__init__
