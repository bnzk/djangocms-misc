# coding: utf-8
from django.conf import settings
from cms.models import Placeholder  # noqa - needed, circular import otherwise
from cms.plugin_rendering import ContentRenderer  # , RenderedPlaceholder

# load conf at startup
from .conf import UntranslatedPlaceholderConf  # noqa
# import signals at startup
from .signals import *  # noqa (will forget to update otherwise!)


def content_renderer__init__(self, request):
    self.__original_init__(request)
    global_untranslated = getattr(settings, 'DJANGOCMS_MISC_UNTRANSLATED_PLACEHOLDERS', None)
    if global_untranslated:
        if global_untranslated in settings.LANGUAGES:
            self.request_language = global_untranslated
        else:
            self.request_language = settings.LANGUAGE_CODE


# hope this is the way to do it!
ContentRenderer.__original_init__ = ContentRenderer.__init__
ContentRenderer.__init__ = content_renderer__init__
