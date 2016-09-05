# coding: utf-8
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from cms_tools.cms_plugins import CMSToolsPluginMixin
from .models import Image


class ImagePlugin(CMSToolsPluginMixin, CMSPluginBase):
    model = Image
    name = _(u'Image')
    render_template = "djangocms_image/image.html"
    fieldsets = [
        (None, {'fields': ('image', 'caption', )})
    ]

plugin_pool.register_plugin(ImagePlugin)
