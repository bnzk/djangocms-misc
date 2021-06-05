# coding: utf-8
from __future__ import unicode_literals

from cms.models import PlaceholderField
from django.urls import reverse
from django.db import models
from django.utils.text import slugify
# from filer.fields.image import FilerImageField
from filer_addons.filer_gui.fields import FilerImageField

from project.managers import PublishedQuerySet
from project.models import PublishedBase, SEOBase


class AppTemplate(PublishedBase, SEOBase, models.Model):
    date = models.DateField()
    title = models.CharField(max_length=255)
    preview_text = models.TextField(blank=True, default='')
    preview_image = FilerImageField(on_delete=models.PROTECT, default=None, null=True)
    content = PlaceholderField(slotname='content')

    objects = PublishedQuerySet.as_manager()

    class Meta:
        ordering = ('-date', )

    def get_slug(self):
        return slugify(self.get_seo_title())

    def get_absolute_url(self):
        return reverse('article_detail', args=(self.id, self.get_slug()))

    def __str__(self):
        return u'%s' % (self.title, )
