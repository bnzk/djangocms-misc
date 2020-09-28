# coding: utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register
class AppTemplateAppHook(CMSApp):
    name = _("AppTemplate App")
    # menus = [CategoryMenu, ]

    def get_urls(self, page=None, language=None, **kwargs):
        return ["apptemplate.urls", ]
