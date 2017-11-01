# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client


class AdminStyleTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username='fred',
            password='test',
            email='test@test.fred',
        )

    def tearDown(self):
        pass

    def test_has_css(self):
        self.client.login(username='fred', password='test')
        url = reverse('admin:index')
        response = self.client.get(url, follow=True)
        self.assertContains(response, 'admin/djangocms_misc/css/admin_style.css')
