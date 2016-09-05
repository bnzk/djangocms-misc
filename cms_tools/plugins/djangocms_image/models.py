# coding: utf-8
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField

from cms_tools.models import CMSToolsPluginBaseModel


@python_2_unicode_compatible
class Image(CMSPlugin, CMSToolsPluginBaseModel):
    caption = models.CharField(max_length=255, blank=True)
    image = FilerImageField(null=True, blank=True)

    def __str__(self):
        return str(self.image)
