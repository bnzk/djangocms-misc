from __future__ import unicode_literals

from django.test import TestCase

from ..models import AppTemplate


# add some basic things (admin list view, detail view, etc)
class AppTemplateTests(TestCase):

    def fetch_objs(self):
        all = AppTemplate.objects.all()
        self.assertEqual(all.count(), 0)
