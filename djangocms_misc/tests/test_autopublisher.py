# -*- coding: utf-8 -*-
from cms.models import Page
from django.test import TestCase, Client, modify_settings

# compat
import django
if django.VERSION[:2] < (1, 10):
    from django.core.urlresolvers import reverse
else:
    from django.urls import reverse


@modify_settings(INSTALLED_APPS={
    'append': 'djangocms_misc.autopublisher',
})
class AutoPublisherTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    # TODO: many autopublisher tests
    def test_save_page(self):
        from cms import api as cms_api
        print("hhhhhh")
        page_test = cms_api.create_page('test', 'base.html', 'en', reverse_id='what')
        page_test.publish('en')
        page_test.reverse_id = 'lucky'
        print("0")
        title_obj = page_test.get_title_obj('en')
        title_obj.title = 'dummy'
        print("1")
        title_obj.save()
        print("maybe get page_test fresh from db!?")
        public_obj = page_test.get_public_object()
        self.assertEqual(page_test.publisher_is_draft, True)
        self.assertEqual(page_test.get_public_object().reverse_id, 'lucky')
        pass

    def test_save_title(self):
        from cms import api as cms_api
        page_test = cms_api.create_page('test', 'base.html', 'en')
        page_test.publish('en')
        title_en = page_test.get_title_obj('en')
        title_en.title = 'another'
        title_en.save()
        self.assertEqual(page_test.publisher_is_draft, True)
        self.assertEqual(page_test.get_public_object().get_title_obj('en').title, 'another')
        pass

    def test_save_plugin(self):
        pass

    def test_move_plugin(self):
        pass

    def test_move_page(self):
        pass

    def test_save_static_placeholder_plugin(self):
        pass

    def test_move_static_placeholder_plugin(self):
        pass
