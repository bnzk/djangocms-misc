# coding: utf-8
from __future__ import unicode_literals

from django import template


register = template.Library()


@register.inclusion_tag('cms_tools/tags/page_link.html', takes_context=True)
def page_link(context, lookup, css_class='', link_text=''):
    context.update({'lookup': lookup, 'css_class': css_class, 'link_text': link_text, })
    return context
