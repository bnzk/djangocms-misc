# coding: utf-8
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField

from cms_tools.models import CMSToolsPluginBase


class Gallery(CMSToolsPluginBase, CMSPlugin):
    pass
