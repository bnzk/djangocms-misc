# -*- coding: utf-8 -*-
from cms.api import create_page, create_title, add_plugin
from cms.test_utils.testcases import CMSTestCase
from cms.tests.test_placeholder import _render_placeholder
from cms.utils.compat.tests import UnittestCompatMixin
from django.core import cache
from sekizai.context import SekizaiContext

from djangocms_misc.tests.test_app.cms_plugins import TestPlugin


class UntranslatedPlaceholderTestCase(CMSTestCase, UnittestCompatMixin):

    def setUp(self):
        u = self._create_user("test", True, True)
        self._login_context = self.login_user_context(u)
        self._login_context.__enter__()

    def tearDown(self):
        self._login_context.__exit__(None, None, None)

    def test_plugins_untranslated(self):
        """ Tests untranslated placeholder configuration """
        page_en = create_page('page_en', 'base.html', 'en')
        title_de = create_title("de", "page_de", page_en)
        placeholder_en = page_en.placeholders.get(slot='untranslated_placeholder')
        placeholder_de = title_de.page.placeholders.get(slot='untranslated_placeholder')
        add_plugin(placeholder_en, TestPlugin, 'en', field1='en field1')

        context_en = SekizaiContext()
        context_en['request'] = self.get_request(language="en", page=page_en)
        context_de = SekizaiContext()
        context_de['request'] = self.get_request(language="de", page=page_en)

        conf = {
            'untranslated_placeholder': {
                'untranslated': True,
                'language_fallback': False,
            },
        }
        # configure untranslated
        with self.settings(CMS_PLACEHOLDER_CONF=conf):
            ## English page should have the text plugin
            content_en = _render_placeholder(placeholder_en, context_en)
            self.assertRegexpMatches(content_en, "^en field1$")
            ## Deutsch page have text due to untranslated
            content_de = _render_placeholder(placeholder_de, context_de)
            self.assertRegexpMatches(content_de, "^en field1$")
            self.assertEqual(len(content_de), 7)

            del(placeholder_en._plugins_cache)
            del(placeholder_de._plugins_cache)
            cache.clear()
            # add another
            add_plugin(placeholder_en, TestPlugin, 'de', field1='de field1')

            # both should have both
            content_de = _render_placeholder(placeholder_de, context_de)
            self.assertRegexpMatches(content_de, "^en field1.*de field1$")
            content_en = _render_placeholder(placeholder_en, context_en)
            self.assertRegexpMatches(content_en, "^en field1.*de field1$")

