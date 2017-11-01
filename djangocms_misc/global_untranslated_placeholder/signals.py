from __future__ import unicode_literals

# from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.dispatch import receiver
# from cms.models import Title
from cms.constants import PUBLISHER_STATE_DIRTY
from cms.signals import post_placeholder_operation, post_publish  # , post_obj_operation

from djangocms_misc.global_untranslated_placeholder.utils import get_untranslated_default_language


if 'djangocms_misc.autopublisher' not in settings.INSTALLED_APPS:

    # published. if not default language, publish default as well
    # if DJANGOCMS_MISC_UNTRANSLATED_MARK_ALL = True, publish all langs (usability thing, mostly)
    @receiver(
        post_publish,
        dispatch_uid="cms_global_untranslated_placeholder_post_publish",
    )
    def post_publish_handler(**kwargs):
        page_instance = kwargs.get('instance', None)
        if not page_instance:
            return
        published_language = kwargs.get('language', settings.LANGUAGE_CODE)
        default_language = get_untranslated_default_language()
        if not published_language == default_language:
            page_instance.publish(default_language)

    # something has changed, if we are not on the default lang, mark current lang/title as as well
    # if DJANGOCMS_MISC_UNTRANSLATED_MARK_ALL = True, mark all languages as dirty!
    @receiver(
        post_placeholder_operation,
        dispatch_uid="cms_global_untranslated_placeholder_post_placeholder_operation",
    )
    def post_ph_operation_handler(sender, operation, request, language, token, origin, **kwargs):
        plugin = None
        if operation == 'change_plugin':
            plugin = kwargs.get('new_plugin', None)
        if not plugin:
            plugin = kwargs.get('plugin', None)
        if not plugin:
            plugin = kwargs.get('plugins', [None, ])[0]
        if plugin:
            placeholder = plugin.placeholder
            if not plugin.language == language:
                # mark current language Title as dirty as well!
                if placeholder.page:
                    title = placeholder.page.get_title_obj(language)
                    title.publisher_state = PUBLISHER_STATE_DIRTY
                    title.save()
