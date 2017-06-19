# coding: utf-8
from __future__ import unicode_literals

from django import template


register = template.Library()


@register.inclusion_tag('djangocms_misc/tags/page_link.html', takes_context=True)
def djangocms_misc_page_link(context, lookup, css_class='', link_text=''):
    context.update({'lookup': lookup, 'css_class': css_class, 'link_text': link_text, })
    return context
