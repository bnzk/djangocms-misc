# coding: utf-8
from django.conf import settings
from cms.models import Placeholder
from cms.plugin_rendering import ContentRenderer, RenderedPlaceholder
from cms.utils.placeholder import get_placeholder_conf


def content_renderer__init__(self, request):
    self.__old_init__(request)
    global_untranslated = getattr(settings, 'DJANGOCMS_MISC_UNTRANSLATED_PLACEHOLDERS', None)
    if global_untranslated:
        if global_untranslated in settings.LANGUAGES:
            self.request_language = global_untranslated
        else:
            self.request_language = settings.LANGUAGE_CODE


ContentRenderer.__old_init__ = ContentRenderer.__init__
ContentRenderer.__init__ = content_renderer__init__


# not needed!

# def render_placeholder(self, placeholder, context, language=None, page=None,
#                        editable=False, use_cache=False, nodelist=None, width=None):
#     template = page.get_template()
#     untranslated = get_placeholder_conf("untranslated", placeholder.slot, template, False)
#     if untranslated:
#         if untranslated in settings.LANGUAGES:
#             language = untranslated
#         else:
#             language = settings.LANGUAGE_CODE
#     print "render!"
#     return self.__old_render_placeholder(placeholder, context, language, page,
#                        editable, use_cache, nodelist, width)
#
#
# ContentRenderer.__old_render_placeholder = ContentRenderer.render_placeholder
# ContentRenderer.render_placeholder = render_placeholder


# def rendered_placeholder__init__(self, placeholder, language, site_id, cached=False,
#                  editable=False, has_content=False):
#     print placeholder
#     print language
#     # 3.4.4
#     self.__old_init__(placeholder, language, site_id, cached, editable)
#     # develop!
#     # self.__old_init__(placeholder, language, site_id, cached, editable, has_content)
#
#
# RenderedPlaceholder.__old_init__ = RenderedPlaceholder.__init__
# RenderedPlaceholder.__init__ = rendered_placeholder__init__
