from django.conf import settings


def get_untranslated_default_language_if_enabled():
    value = getattr(settings, 'DJANGOCMS_MISC_UNTRANSLATED_PLACEHOLDERS', None)
    if value and value is not True:
        for lang_tuple in settings.LANGUAGES:
            if lang_tuple[0] == value:
                return value
    if value:
        return settings.LANGUAGE_CODE
    return None
