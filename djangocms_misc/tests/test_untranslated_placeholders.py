# -*- coding: utf-8 -*-
from cms.api import create_page, create_title, add_plugin
from django.test import Client
from django.test.testcases import TestCase

from djangocms_misc.tests.test_app.cms_plugins import TestPlugin


class UntranslatedPlaceholderTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        # u = self._create_user("test", True, True)
        # self._login_context = self.login_user_context(u)
        # self._login_context.__enter__()

    def tearDown(self):
        pass
        # self._login_context.__exit__(None, None, None)

    def test_basic(self):
        """ Tests untranslated placeholder configuration """
        page = create_page('page_en', 'base.html', 'en')
        create_title("de", "page_de", page)
        placeholder_en = page.placeholders.get(slot='untranslated_placeholder')
        add_plugin(placeholder_en, TestPlugin, 'en', field1='en field1')
        page.publish('en')
        page.publish('de')

        # English page should have the text plugin
        content_en = self.client.get(page.get_absolute_url())
        self.assertRegexpMatches(str(content_en.content), "en field1")
        # Deutsch page have text due to untranslated
        content_de = self.client.get(page.get_absolute_url('de'))
        self.assertRegexpMatches(str(content_de.content), "en field1")

    def test_publish_non_default_language(self):
        """
        test if a publish in a no default language also works
        """
        page = create_page('page_en', 'base.html', 'en')
        create_title("de", "page_de", page)
        placeholder_en = page.placeholders.get(slot='untranslated_placeholder')
        plugin = add_plugin(placeholder_en, TestPlugin, 'en', field1='starting different')
        page.publish('en')
        page.publish('de')
        plugin.field1 = 'en field1'
        plugin.save()
        page.publish('de')

        # English page should have the text plugin
        content_en = self.client.get(page.get_absolute_url())
        self.assertRegexpMatches(str(content_en.content), "en field1")
        # Deutsch page have text due to untranslated
        content_de = self.client.get(page.get_absolute_url('de'))
        self.assertRegexpMatches(str(content_de.content), "en field1")
