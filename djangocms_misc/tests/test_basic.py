# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cms.api import create_page, create_title, add_plugin
from django.contrib.auth.models import User
from django.test import TestCase, Client, modify_settings

from djangocms_misc.basic.templatetags.djangocms_misc_tags import djangocms_misc_placeholder_empty
from djangocms_misc.tests.test_app.cms_plugins import TestPlugin


class BasicAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username='fred',
            password='test',
            email='test@test.fred',
        )

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

    def test_placeholder_empty_tag(self):
        page = create_page('page_en', 'base.html', 'en')
        page.reverse_id = 'test'
        create_title("de", "page_de", page)
        placeholder_en = page.placeholders.get(slot='untranslated_placeholder')
        self.assertEqual(djangocms_misc_placeholder_empty(placeholder_en), True)
        self.assertEqual(djangocms_misc_placeholder_empty(page, 'untranslated_placeholder'), True)
        plugin = add_plugin(placeholder_en, TestPlugin, 'en', )
        # plugin.field1 = 'en field1'
        plugin.field1_en = 'en field1'
        plugin.save()
        self.assertEqual(djangocms_misc_placeholder_empty(placeholder_en), False)
        self.assertEqual(djangocms_misc_placeholder_empty(page, 'untranslated_placeholder'), False)

    def test_get_from_page_content_tag(self):
        """
        Tests if content is fetched
        """
        page = create_page('page_en', 'base.html', 'en')
        page.reverse_id = 'test'
        create_title("de", "page_de", page)
        placeholder_en = page.placeholders.get(slot='untranslated_placeholder')
        plugin = add_plugin(placeholder_en, TestPlugin, 'en', )
        # plugin.field1 = 'en field1'
        plugin.field1_en = 'en field1'
        plugin.save()
        page.publish('en')
        page.publish('de')
        # untranslated placeholder is enabled, so the content shoudl appear de/en 2x each
        response = self.client.get(page.get_absolute_url('en'))
        self.assertContains(response, 'en field1', 5)
        response = self.client.get(page.get_absolute_url('de'))
        self.assertContains(response, 'en field1', 5)
        # also, draft mode!
        self.client.login(username='fred', password='test')
        response = self.client.get(page.get_absolute_url('en') + '?edit')
        # one more, in the structure mode/plugin representation
        self.assertContains(response, ': en field1', 5)

    def test_language_tabs_admin_mixin(self):
        # TODO: language tabs tests
        pass

    def test_redirect_first_subpage_middleware(self):
        page_home = create_page('home', 'base.html', 'en')
        page_home.publish('en')
        page_parent = create_page('parent', 'base.html', 'en', redirect='/firstchild')
        page_parent.publish('en')
        page_child1 = create_page('child1', 'base.html', 'en', parent=page_parent)
        page_child1.publish('en')
        page_child2 = create_page('child2', 'base.html', 'en', parent=page_parent)
        page_child2.publish('en')
        # get the parent
        response = self.client.get(page_parent.get_absolute_url('en'))
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, '/en/parent/child1/')
        # check for some false positives
        response = self.client.get(page_child1.get_absolute_url('en'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(page_home.get_absolute_url('en'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(page_child2.get_absolute_url('en'))
        self.assertEqual(response.status_code, 200)
        # 404 still ok?
        response = self.client.get('/en/absolutely-not-exising/22/')
        self.assertEqual(response.status_code, 404)

    @modify_settings(MIDDLEWARE={
        'append': 'djangocms_misc.basic.middleware.PasswordProtectedMiddleware',
    })
    def test_password_protected_middleware(self):
        page_home = create_page('home', 'base.html', 'en')
        page_home.reverse_id = 'home'
        page_home.save()
        page_home.publish('en')
        response = self.client.get(page_home.get_absolute_url('en'))
        self.assertEqual(response.status_code, 302)
        pass

    def test_bot404_middleware(self):
        # TODO: tests
        pass
