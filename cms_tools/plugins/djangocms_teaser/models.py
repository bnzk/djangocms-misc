# coding: utf-8
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField

from bodenschatz.models.base import LinkBase
# from .cms_plugins import HEADER_TEASER_TYPE_CHOICES, TEASER_TYPE_CHOICES


ALL_TEASER_TYPE_CHOICES = (
    # header
    ('right', _('Text Rechts')),
    ('middle', _('Text Mitte')),
    # into container
    ('scroll', _('Scroll (Quad) Teaser')),
    ('product', _('Produkte Teaser')),
    ('cooperation', _('Kooperations Teaser')),
    # no teaser! ;
    ('meet', _('Please meet')),
)

COLOUR_CHOICES = (
    ('black', _("Schwarz"), ),
    ('white', _("Weiss"), ),
)

SECTION_TYPE_CHOICES = (
    ('default', _('Normal')),
    ('scroll', _('Scroll')),
)


@python_2_unicode_compatible
class Teaser(CMSPlugin, LinkBase):
    colour = models.CharField(max_length=25, blank=False, default='black', choices=COLOUR_CHOICES)
    teaser_type = models.CharField(max_length=25, blank=True, default='normal',
                                   choices=ALL_TEASER_TYPE_CHOICES)
    mini_title = models.CharField(max_length=255, blank=True, default='')
    title = models.CharField(max_length=255, blank=False, default='')
    full_name = models.CharField(verbose_name='Name', max_length=255, blank=True, default='')
    body = models.TextField(verbose_name=_(u'Text'), blank=True)
    image = FilerImageField(blank=False, null=True, default=None, related_name='teaser_image')

    def __str__(self):
        if self.title:
            return u'%s' % (self.title, )


@python_2_unicode_compatible
class TeaserSection(CMSPlugin):
    section_type = models.CharField(max_length=25, blank=True, default='normal',
                                   choices=SECTION_TYPE_CHOICES)
    title = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return "Teaser Sektion %s" % self.title