# coding: utf-8
from __future__ import unicode_literals

from ckeditor.fields import RichTextField
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField

from cms_tools.models import CMSToolsPluginBaseModel


IMAGETEXT_LAYOUT_CHOICES = (
    ('textleft_small', _('Text links, klein')),
    ('textright_small', _('Text rechts, klein')),
    ('textleft_big', _('Text links, gross')),
    ('textright_big', _('Text rechts, gross')),
)


@python_2_unicode_compatible
class ImageText(CMSPlugin, CMSToolsPluginBaseModel):
    caption = models.CharField(max_length=255, blank=True)
    image = FilerImageField(null=True, blank=True)
    body = RichTextField(blank=True, default='')

    def __str__(self):
        hidden = self.get_hidden_state_text()
        truncated = Truncator(strip_tags(self.body).replace('&shy;', '')).words(3, truncate="...")
        return "%s %s" % (truncated, hidden, )
