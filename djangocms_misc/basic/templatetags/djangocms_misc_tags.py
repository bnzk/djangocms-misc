# coding: utf-8
from __future__ import unicode_literals

from django import template


register = template.Library()


@register.inclusion_tag('djangocms_misc/tags/page_link.html', takes_context=True)
def djangocms_misc_page_link(context, lookup, css_class='', link_text=''):
    context.update({'lookup': lookup, 'css_class': css_class, 'link_text': link_text, })
    return context


DJANGCMS_MISC_GET_FROM_PAGE = {
    'video_instance': {
        'placeholders': ('Inhalt',),
        'plugins': {
            'YoutubeVideoPlugin': [],
        }
    },
    'image': {
        'placeholders': ('Inhalt', ),
        'plugins': {
            'ImagePlugin': ('image', 'preview_image'),
            'HeaderPlugin': ('image', ),
        }
    },
    'text': {
        'placeholders': ('Inhalt',),
        'plugins': {
            'ImagePlugin': ('image', 'preview_image'),
            'HeaderPlugin': ('image',),
        }
    },
}


@register.simple_tag(takes_context=True)
def djangocms_misc_get_from_page_content(context, page, config_name='image'):
    image = None
    config = DJANGCMS_MISC_GET_FROM_PAGE.get(config_name, None)
    if not page:
        request = context['request']
        page = getattr(request, 'current_page', None)
    if page and config:
        image = get_from_page_content(page, config)
        return image
    return None


def get_from_page_content(page, config):
    placeholders = page.get_placeholders()
    to_scan_placeholders = config.get('placeholders')
    to_scan_plugins = config.get('plugins')
    for slot_name in to_scan_placeholders:
        placeholder = placeholders.filter(slot=slot_name)
        if placeholder.count():
            plugins = placeholder[0].get_plugins()
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
    return None