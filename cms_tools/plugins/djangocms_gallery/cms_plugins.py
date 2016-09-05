# coding: utf-8
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import Image


class GalleryPlugin(CMSPluginBase):
    model = Gallery
    name = _(u'Gallery')
    render_template = "djangocms_gallery/gallery.html"
    allow_children = True
    child_classes = ('GalleryImagePlugin', )

plugin_pool.register_plugin(GalleryPlugin)
