# coding: utf-8
import copy

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

import settings as my_settings


class CMSToolsPluginMixin(object):
    def render(self, context, instance, placeholder):
        context = super(CMSToolsPluginMixin, self).render(context, instance, placeholder)
        if not context.get('request').toolbar.edit_mode and instance.hide:
            self.render_template = 'cms_tools/hide.html'
        return context

    def get_fieldsets(self, request, obj=None):
        # class level attribute, let's deep copy it!
        fieldsets = copy.deepcopy(super(CMSToolsPluginMixin, self).get_fieldsets(request, obj))
        if not len(fieldsets):
            fieldsets = []
        fieldsets.append(my_settings.CMS_TOOLS_PLUGINS_ADVANCED_FIELDSET)
        return fieldsets