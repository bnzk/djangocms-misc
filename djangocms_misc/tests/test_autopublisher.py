# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase, Client


class AutoPublisherTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    # TODO: many autopublisher tests
    def test_save_page(self):
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
