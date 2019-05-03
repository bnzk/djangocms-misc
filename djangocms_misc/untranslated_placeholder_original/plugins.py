# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import groupby
from operator import attrgetter

from cms.utils import get_language_from_request
from cms.utils.i18n import get_fallback_languages
from cms.utils.moderator import get_cmsplugin_queryset
from cms.utils.placeholder import get_placeholder_conf
from cms.utils.plugins import create_default_plugins, build_plugin_tree
from cms.utils.plugins import downcast_plugins

from djangocms_misc.utils.edit_mode import is_edit_mode


def assign_plugins(request, placeholders, template, lang=None, is_fallback=False):
    """
    Fetch all plugins for the given ``placeholders`` and
    cast them down to the concrete instances in one query
    per type.
    """
    if not placeholders:
        return
    placeholders = tuple(placeholders)
    lang = lang or get_language_from_request(request)
    translated_placeholders = []
    untranslated_placeholders = []
    for placeholder in placeholders:
        if get_placeholder_conf("untranslated", placeholder.slot, template, False):
            untranslated_placeholders.append(placeholder)
        else:
            translated_placeholders.append(placeholder)
    _assign_plugins(request, translated_placeholders, template, lang, is_fallback)
    _assign_plugins(request, untranslated_placeholders, template, lang, is_fallback, True)


def _assign_plugins(request, placeholders, template, lang=None, is_fallback=False,
                    untranslated=False):
    qs = get_cmsplugin_queryset(request)
    if untranslated:
        qs = qs.filter(placeholder__in=placeholders)
    else:
        qs = qs.filter(placeholder__in=placeholders, language=lang)
    plugins = list(qs.order_by('placeholder', 'path'))
    fallbacks = defaultdict(list)
    # If no plugin is present in the current placeholder we loop in the fallback languages
    # and get the first available set of plugins
    if not (is_fallback or untranslated) \
            and not (hasattr(request, 'toolbar') and is_edit_mode(request.toolbar)):
        disjoint_placeholders = (ph for ph in placeholders
                                 if all(ph.pk != p.placeholder_id for p in plugins))
        for placeholder in disjoint_placeholders:
            if get_placeholder_conf("language_fallback", placeholder.slot, template, True):
                for fallback_language in get_fallback_languages(lang):
                    _assign_plugins(
                        request,
                        (placeholder,),
                        template,
                        fallback_language,
                        is_fallback=True
                    )
                    fallback_plugins = placeholder._plugins_cache
                    if fallback_plugins:
                        fallbacks[placeholder.pk] += fallback_plugins
                        break

    # These placeholders have no fallback
    non_fallback_phs = [ph for ph in placeholders if ph.pk not in fallbacks]
    # If no plugin is present in non fallback placeholders, create default plugins if enabled)
    if not plugins:
        plugins = create_default_plugins(request, non_fallback_phs, template, lang)
    plugins = downcast_plugins(plugins, non_fallback_phs, request=request)
    # split the plugins up by placeholder
    # Plugins should still be sorted by placeholder
    plugin_groups = dict((key, list(plugins))
                         for key, plugins in groupby(plugins, attrgetter('placeholder_id')))
    all_plugins_groups = plugin_groups.copy()
    for group in plugin_groups:
        plugin_groups[group] = build_plugin_tree(plugin_groups[group])
    groups = fallbacks.copy()
    groups.update(plugin_groups)
    for placeholder in placeholders:
        # This is all the plugins.
        setattr(placeholder, '_all_plugins_cache', all_plugins_groups.get(placeholder.pk, []))
        # This one is only the root plugins.
        setattr(placeholder, '_plugins_cache', groups.get(placeholder.pk, []))
