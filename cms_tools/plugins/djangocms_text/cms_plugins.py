# coding: utf-8
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from cms_tools.cms_plugins import CMSToolsPluginMixin
from .models import Text


class TextPlugin(CMSToolsPluginMixin, CMSPluginBase):
    model = Text
    name = _(u'Text')
    render_template = "djangocms_text/text.html"
    fieldsets = [
        (None, {'fields': ('body', )}),
    ]

plugin_pool.register_plugin(TextPlugin)