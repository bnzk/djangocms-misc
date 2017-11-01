from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from modeltranslation.admin import TranslationAdmin

from djangocms_misc.basic.admin import LanguageTabsMixin
from djangocms_misc.tests.test_app.models import TestPluginModel


class TestPlugin(LanguageTabsMixin, TranslationAdmin, CMSPluginBase):
    model = TestPluginModel
    render_template = 'test_app/testplugin.html'


plugin_pool.register_plugin(TestPlugin)
