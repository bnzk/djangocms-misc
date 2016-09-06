# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class CMSToolsPluginBaseModel(models.Model):
    style = models.CharField(max_length=31, blank=True, default='')
    anchor = models.SlugField(blank=True, default='')
    hide = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def get_hidden_state_text(self):
        if self.hide:
            return "(%s)" % _("HIDDEN")
        else:
            return ""