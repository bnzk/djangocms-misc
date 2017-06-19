# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from formfieldstash.tests.utils.django_utils import create_superuser
from formfieldstash.tests.utils.selenium_utils import SeleniumTestCase, CustomWebDriver
from formfieldstash.tests.test_app.models import TestModelSingle, TestModelAdvanced


class FormFieldStashAdminTests(SeleniumTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_app_index_get(self):
        self.login()
        self.open(reverse('admin:index'))
