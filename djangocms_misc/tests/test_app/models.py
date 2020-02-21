from __future__ import unicode_literals

from cms.models import CMSPlugin
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class TestPluginModel(CMSPlugin):
    field1 = models.CharField(max_length=64, default='', blank=False)
    field_date = models.DateField(default=None, null=True, )
    field_datetime = models.DateTimeField(default=None, null=True, )
    field_time = models.TimeField(default=None, null=True, )

    def __str__(self):
        return self.field1


@python_2_unicode_compatible
class TestModel(models.Model):
    field0 = models.CharField(max_length=64, default='', blank=True)
    field1 = models.CharField(max_length=64, default='', blank=False)
    field2 = models.CharField(max_length=64, default='', blank=True)

    def __str__(self):
        return self.field1


@python_2_unicode_compatible
class TestInlineModel(models.Model):
    testmodel = models.ForeignKey(TestModel, on_delete=models.CASCADE)
    field1 = models.CharField(max_length=64, default='', blank=False)
    field2 = models.CharField(max_length=64, default='', blank=True)

    def __str__(self):
        return self.field1
