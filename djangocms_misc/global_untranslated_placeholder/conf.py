from appconf import AppConf


class UntranslatedPlaceholderConf(AppConf):
    UNTRANSLATED_PLACEHOLDERS = False

    class Meta:
        prefix = 'djangocms_misc'
