# -*- coding: utf-8 -*-
from cms.api import create_page, create_title, add_plugin
from django.test import TestCase, Client

from djangocms_misc.tests.test_app.cms_plugins import TestPlugin


class BasicAppTests(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_page_link_tag(self):
        page_test = create_page('test', 'base.html', 'en')
        page_test.publish('en')
        page_home = create_page('home', 'base.html', 'en')
        page_home.reverse_id = 'home'
        page_home.save()
        page_home.publish('en')
        response = self.client.get(page_test.get_absolute_url('en'))
        self.assertContains(response, '/en/home/')
        self.assertContains(response, '/home/">link text HOME')
        self.assertContains(response, 'class="button" href="/en/home/">')

    def test_get_from_page_content_tag(self):
        """
        Tests if content is fetched
        """
        page = create_page('page_en', 'base.html', 'en')
        create_title("de", "page_de", page)
        placeholder_en = page.placeholders.get(slot='untranslated_placeholder')
        add_plugin(placeholder_en, TestPlugin, 'en', field1='en field1')
        page.publish('en')
        page.publish('de')

        # untranslated placeholder is enabled, so the content shoudl appear de/en 2x each
        response = self.client.get(page.get_absolute_url('en'))
        self.assertContains(response, 'en field1', 2)
        response = self.client.get(page.get_absolute_url('de'))
        self.assertContains(response, 'en field1', 2)
