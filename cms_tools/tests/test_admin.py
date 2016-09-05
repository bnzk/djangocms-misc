# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from formfieldstash.tests.utils.django_utils import create_superuser
from formfieldstash.tests.utils.selenium_utils import SeleniumTestCase, CustomWebDriver
from formfieldstash.tests.test_app.models import TestModelSingle, TestModelAdvanced


class FormFieldStashAdminTests(SeleniumTestCase):
    def setUp(self):
        self.single_empty = TestModelSingle()
        self.single_empty.save()
        self.single = TestModelSingle(**{'selection': 'octopus', })
        self.single.save()
        self.advanced_empty = TestModelAdvanced()
        self.advanced_empty.save()
        self.advanced = TestModelAdvanced(**{'set': 'set1', })
        self.advanced.save()
        self.superuser = create_superuser()
        # Instantiating the WebDriver will load your browser
        self.wd = CustomWebDriver()

    def tearDown(self):
        self.wd.quit()

    def test_app_index_get(self):
        self.login()
        self.open(reverse('admin:index'))
        self.wd.find_css(".app-test_app")

    def test_single_stash_empty(self):
        self.login()
        self.open(reverse('admin:test_app_testmodelsingle_change', args=[self.single_empty.id]))
        horse = self.wd.find_css("div.field-horse")
        self.assertFalse(horse.is_displayed())
        bear = self.wd.find_css("div.field-bear")
        self.assertFalse(bear.is_displayed())
        octo = self.wd.find_css("div.field-octopus")
        self.assertFalse(octo.is_displayed())

    def test_single_stash(self):
        self.login()
        self.open(reverse('admin:test_app_testmodelsingle_change', args=[self.single.id]))
        horse = self.wd.find_css("div.field-horse")
        self.assertFalse(horse.is_displayed())
        bear = self.wd.find_css("div.field-bear")
        self.assertFalse(bear.is_displayed())
        octo = self.wd.find_css("div.field-octopus")
        self.assertTrue(octo.is_displayed())
        # change select value
        self.wd.find_css("div.field-selection select > option[value=horse]").click()
        horse = self.wd.find_css("div.field-horse")
        self.assertTrue(horse.is_displayed())
        octo = self.wd.find_css("div.field-octopus")
        self.assertFalse(octo.is_displayed())

    def test_multi_stash_empty(self):
        self.login()
        self.open(reverse('admin:test_app_testmodeladvanced_change', args=[self.advanced_empty.id]))
        inline = self.wd.find_css("#testinlinemodel_set-group")
        self.assertFalse(inline.is_displayed())
        f11 = self.wd.find_css("div.field-set1_1")
        self.assertFalse(f11.is_displayed())
        f31 = self.wd.find_css("div.field-set3_1")
        self.assertFalse(f31.is_displayed())

    def test_multi_stash(self):
        self.login()
        self.open(reverse('admin:test_app_testmodeladvanced_change', args=[self.advanced.id]))
        inline = self.wd.find_css("#testinlinemodel_set-group")
        self.assertTrue(inline.is_displayed())
        f11 = self.wd.find_css("div.field-set1_1")
        self.assertTrue(f11.is_displayed())
        f31 = self.wd.find_css("div.field-set3_1")
        self.assertFalse(f31.is_displayed())

