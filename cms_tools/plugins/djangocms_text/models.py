# coding: utf-8
from __future__ import unicode_literals

from ckeditor.fields import RichTextField
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import strip_tags
from django.utils.text import Truncator

from django.utils.translation import ugettext_lazy as _
from cms.models.pluginmodel import CMSPlugin

from cms_tools.models import CMSToolsPluginBaseModel


@python_2_unicode_compatible
class Text(CMSPlugin, CMSToolsPluginBaseModel):
    body = RichTextField(blank=True, default='')

    def __str__(self):
        return Truncator(strip_tags(self.body).replace('&shy;', '')).words(3, truncate="...")
