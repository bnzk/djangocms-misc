# coding: utf-8
from __future__ import unicode_literals

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django import forms
from django.utils.translation import ugettext_lazy as _
from formfieldstash.admin import FormFieldStashMixin

from .models import Teaser, TeaserSection
from bodenschatz.models.base import LINK_FIELDS


HEADER_TEASER_TYPE_CHOICES = (
    ('right', _('Text Rechts')),
    ('middle', _('Text Mitte')),
)

TEASER_TYPE_CHOICES = (
    ('scroll', _('Scroll (Quad) Teaser')),
    ('product', _('Produkte Teaser')),
    ('cooperation', _('Kooperations Teaser')),
)

# nope
# class HeaderTeaserForm(forms.ModelForm):
    # teaser_type = forms.ChoiceField(choices=HEADER_TEASER_TYPE_CHOICES)


class TeaserBase(FormFieldStashMixin, CMSPluginBase):
    module = _('Teaser')
    model = Teaser
    name = _(u'Override! Teaser')
    render_template = "djangocms_teaser/teaser.html"
    text_enabled = False
    fieldsets = (
        (None, { 'fields': ('teaser_type', 'title', 'body', 'image', )} ),
        (_('Link'), { 'fields': LINK_FIELDS} ),
    )
    single_formfield_stash = ('link_type', )

    def render(self, context, instance, placeholder):
        context = super(TeaserBase, self).render(context, instance, placeholder)
        if getattr(self, 'teaser_size', None):
            context['teaser_size'] = self.teaser_size
        return context


class HeaderTeaserPlugin(TeaserBase):
    name = _(u'Header Teaser')
    render_template = "djangocms_teaser/header_teaser.html"
    fieldsets = (
        (None, { 'fields': ('teaser_type', 'colour', 'title', 'body', 'image', )} ),
        (_('Link'), { 'fields': LINK_FIELDS} ),
    )
    formfield_stash = {
        'teaser_type': {
            'meet_black': ('name',),
            'meet_white': ('name',),
            }
    }
    def formfield_for_dbfield(self, db_field, *args, **kwargs):
        if db_field.name == 'teaser_type':
            kwargs['choices'] = HEADER_TEASER_TYPE_CHOICES
        return super(HeaderTeaserPlugin, self).formfield_for_dbfield(db_field, *args, **kwargs)


class CooperationHeaderForm(forms.ModelForm):
    teaser_type = forms.CharField(initial='meet', widget=forms.HiddenInput())


class CooperationHeaderPlugin(CMSPluginBase):
    form = CooperationHeaderForm
    model = Teaser
    name = _(u'Cooperation Header')
    render_template = "djangocms_teaser/header_cooperation.html"
    fieldsets = (
        (None, { 'fields': ('teaser_type', 'colour', 'title', 'full_name', 'body', 'image', )} ),
    )


class ScrollTeaserForm(forms.ModelForm):
    teaser_type = forms.CharField(initial='scroll', widget=forms.HiddenInput())


class ScrollTeaserPlugin(TeaserBase):
    form = ScrollTeaserForm
    name = _(u'Scroll Teaser')
    render_template = "djangocms_teaser/teaser.html"
    require_parent = True
    teaser_size = '300x300'


class CooperationTeaserForm(forms.ModelForm):
    teaser_type = forms.CharField(initial='cooperation', widget=forms.HiddenInput())


class CooperationTeaserPlugin(TeaserBase):
    form = CooperationTeaserForm
    name = _(u'Cooperation Teaser')
    render_template = "djangocms_teaser/teaser_cooperation.html"
    require_parent = True
    teaser_size = '450x512'
    fieldsets = (
        (None, { 'fields': ('teaser_type', 'colour', 'title' , 'body', 'image', )} ),
        (_('Link'), { 'fields': LINK_FIELDS} ),
    )

class ProductTeaserForm(forms.ModelForm):
    teaser_type = forms.CharField(initial='product', widget=forms.HiddenInput())


class ProductTeaserPlugin(TeaserBase):
    form = ProductTeaserForm
    name = _(u'Product Teaser')
    render_template = "djangocms_teaser/teaser_product.html"
    require_parent = True
    teaser_size = '400x400'
    fieldsets = (
        (None, { 'fields': ('teaser_type', 'title', 'full_name', 'body', 'image', )} ),
        (_('Link'), { 'fields': LINK_FIELDS} ),
    )


class DefaultTeaserSectionForm(forms.ModelForm):
    section_type = forms.CharField(initial='default', widget=forms.HiddenInput())


class DefaultTeaserSectionPlugin(CMSPluginBase):
    form = DefaultTeaserSectionForm
    module = _('Teaser')
    model = TeaserSection
    child_classes = ('CooperationTeaserPlugin', 'ProductTeaserPlugin')
    allow_children = True
    name = _(u'Teaser Sektion/Container')
    render_template = "djangocms_teaser/teaser_section.html"


class ScrollTeaserSectionForm(forms.ModelForm):
    section_type = forms.CharField(initial='scroll', widget=forms.HiddenInput())


class ScrollTeaserSectionPlugin(CMSPluginBase):
    form = ScrollTeaserSectionForm
    module = _('Teaser')
    model = TeaserSection
    child_classes = ('ScrollTeaserPlugin', )
    allow_children = True
    name = _(u'Scroll Teaser Sektion/Container')
    render_template = "djangocms_teaser/teaser_section.html"


plugin_pool.register_plugin(HeaderTeaserPlugin)
plugin_pool.register_plugin(CooperationHeaderPlugin)
plugin_pool.register_plugin(DefaultTeaserSectionPlugin)
plugin_pool.register_plugin(ScrollTeaserSectionPlugin)
plugin_pool.register_plugin(ScrollTeaserPlugin)
plugin_pool.register_plugin(CooperationTeaserPlugin)
plugin_pool.register_plugin(ProductTeaserPlugin)