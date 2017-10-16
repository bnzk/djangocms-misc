# -*- coding: utf-8 -*-
from cms.api import create_page
from django.test import TestCase, Client


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

    def get_from_page_content_tag(self):
        pass
