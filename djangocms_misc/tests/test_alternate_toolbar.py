# -*- coding: utf-8 -*
from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
from django.test import TestCase, Client, override_settings
from cms.api import create_page


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

    @override_settings(DEBUG=True)
    def test_toolbar_renders_without_pages(self):
        """
        weird recursion bug, only when DEBUG=True and without any pages
        edge case, but annonying when setting up a new site
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.client.login(username='fred', password='test')
        response = self.client.get('/en/admin/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/en/?edit')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/en/not-existing-at-all/')
        self.assertEqual(response.status_code, 404)

    def test_toolbar_renders_has_links(self):
        """
        basic tests. check for some links and if it renders at all
        """
        self.client.login(username='fred', password='test')
        page = create_page('test', 'base.html', 'en')
        page.publish('en')

        url = page.get_absolute_url()
        response = self.client.get(url)
        self.assertRegexpMatches(str(response.content), "\"/en/admin/auth/\"")
        self.assertRegexpMatches(str(response.content), "\"/en/admin/password_change/\"")
