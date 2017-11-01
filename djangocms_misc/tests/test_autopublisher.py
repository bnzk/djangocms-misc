# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase, Client


class DoesItStillRunTests(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_app_index_get(self):
        # self.login()
        self.client.get(reverse('admin:index'))
