# -*- coding: utf-8 -*-
from cms.api import create_page
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client


class AlternateToolbarTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username='fred',
            password='test',
            email='test@test.fred',
        )

    def tearDown(self):
        pass

    def test_toolbar_renders_has_links(self):
        self.client.login(username='fred', password='test')
        page = create_page('test', 'base.html', 'en')
        page.publish('en')

        response = self.client.get(page.get_absolute_url())
        self.assertRegexpMatches(str(response.content), "\"/en/admin/auth/\"")
        self.assertRegexpMatches(str(response.content), "\"/en/admin/password_change/\"")

