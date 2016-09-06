# coding: utf-8
from __future__ import unicode_literals

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import ColumnContainer, Column


class ColumnContainerPlugin(CMSPluginBase):
    model = ColumnContainer
    name = _('Mehrere Spalten')
    render_template = "djangocms_columns/container.html"
    allow_children = True
    child_classes = ('ColumnPlugin', )

plugin_pool.register_plugin(ColumnContainerPlugin)


class ColumnPlugin(CMSPluginBase):
    model = Column
    name = _('Spalte')
    render_template = "djangocms_columns/column.html"
    require_parent = True
    parent_classes = ('ColumnContainerPlugin', )
    allow_children = True
    # TODO: make it via settings
    # child_classes = ('whateverPlugin')

plugin_pool.register_plugin(ColumnContainerPlugin)
