# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase


class DoesItStillRunTests(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_app_index_get(self):
        # self.login()
        self.open(reverse('admin:index'))
