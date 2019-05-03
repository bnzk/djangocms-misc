# coding: utf-8
from __future__ import unicode_literals

from cms.models import Page
from django.conf import settings
from django import template

from djangocms_misc.utils.edit_mode import is_edit_mode

register = template.Library()


@register.inclusion_tag('djangocms_misc/tags/page_link.html', takes_context=True)
def djangocms_misc_page_link(context, lookup, css_class='', link_text='', link_text_attr=''):
    """
    link_text_attr is not working (yet)
    """
    if not link_text_attr:
        link_text_attr = 'title'
    context.update({
        'lookup': lookup,
        'css_class': css_class,
        'link_text': link_text,
        'link_text_attr': link_text_attr,
    })
    return context


@register.simple_tag(takes_context=True)
def djangocms_misc_get_from_page_content(context, config_name, page_lookup=None):
    config = settings.DJANGOCMS_MISC_GET_FROM_PAGE_CONTENT.get(config_name, None)
    request = context['request']
    page = None
    if isinstance(page_lookup, Page):
        page = page_lookup
    else:
        try:
            page_id = int(page_lookup)
            page = Page.objects.get(pk=page_id)
        except (TypeError, ValueError, Page.DoesNotExist) as e:
            pass
        try:
            page_reverse_id = str(page_lookup)
            qs = Page.objects.all()
            if is_edit_mode(request.toolbar):
                qs = qs.drafts()
            else:
                qs = qs.public()
            page = qs.get(reverse_id=page_reverse_id)
        except (ValueError, Page.DoesNotExist) as e:
            pass
        if not page:
            page = getattr(request, 'current_page', None)
    if page and config:
        content = get_from_page_content(request, config, page)
        return content
    return ''


def get_from_page_content(request, config, page):
    placeholders = page.get_placeholders()
    to_scan_placeholders = config.get('placeholders')
    to_scan_plugins = config.get('plugins')
    for slot_name in to_scan_placeholders:
        placeholder = placeholders.filter(slot=slot_name)
        if placeholder.count():
            language = request.LANGUAGE_CODE
            if 'djangocms_misc.global_untranslated_placeholder' in settings.INSTALLED_APPS and\
                    settings.DJANGOCMS_MISC_UNTRANSLATED_PLACEHOLDERS:
                from djangocms_misc.global_untranslated_placeholder.utils import \
                    get_untranslated_default_language
                language = get_untranslated_default_language()
            plugins = placeholder[0].get_plugins(language).order_by('position')
            for plugin in plugins:
                if plugin.plugin_type in to_scan_plugins:
                    instance, plugin_cls = plugin.get_plugin_instance()
                    to_scan_fields = to_scan_plugins[plugin.plugin_type]
                    if len(to_scan_fields):
                        for field in to_scan_fields:
                            if instance and getattr(instance, field, None):
                                content = getattr(instance, field)
                                return content
                    else:
                        return instance
    return ''
