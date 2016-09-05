# coding: utf-8
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from cms_tools.cms_plugins import CMSToolsPluginMixin
from .models import ImageText


class ImageTextPlugin(CMSToolsPluginMixin, CMSPluginBase):
    model = ImageText
    name = _(u'Bild + Text')
    render_template = "djangocms_imagetext/imagetext.html"
    text_enabled = False
    fieldsets = [
        (None, {'fields': ('image', 'caption', 'body', )})
    ]

plugin_pool.register_plugin(ImageTextPlugin)
