# coding: utf-8
from cms.models import Placeholder  # noqa - needed, circular import otherwise
from cms.plugin_rendering import ContentRenderer  # , RenderedPlaceholder


try:
    # cms 3.5 or 3.7+
    from cms.plugin_rendering import StructureRenderer
except ImportError:
    StructureRenderer = None


# load conf at startup
from .conf import UntranslatedPlaceholderConf  # noqa
# import signals at startup
from .signals import *  # noqa (will forget to update otherwise!)
from .utils import get_untranslated_default_language_if_enabled


def new_renderer__init__(self, request):
    self.__original_init__(request)
    lang = get_untranslated_default_language_if_enabled()
    if lang:
        self.request_language = lang


# monkey patch!
# for normal plugin rendering.
ContentRenderer.__original_init__ = ContentRenderer.__init__
ContentRenderer.__init__ = new_renderer__init__


def new_structure_render_placeholder(self, placeholder, language, page=None):
    language = language or self.request_language
    return self.__original_render_placeholder(placeholder, language, page)


if StructureRenderer:
    # for structure mode
    StructureRenderer.__original_init__ = StructureRenderer.__init__
    StructureRenderer.__init__ = new_renderer__init__
    StructureRenderer.__original_render_placeholder = StructureRenderer.render_placeholder
    StructureRenderer.render_placeholder = new_structure_render_placeholder
