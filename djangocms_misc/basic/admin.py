from __future__ import unicode_literals

from django.conf import settings


# thx to @wullerot https://gist.github.com/wullerot/9fe3151101e57a9ee6fadb3cababb619
class LanguageTabsMixin(object):
    change_form_template = 'admin/djangocms_misc/modeltranslation_lang_tabs_change_form.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        context = extra_context or {}
        context['tab_languages'] = settings.LANGUAGES
        return super(LanguageTabsMixin, self).change_view(
            request,
            object_id=object_id,
            form_url=form_url,
            extra_context=context
        )

    def add_view(self, request, form_url='', extra_context=None):
        context = extra_context or {}
        context['tab_languages'] = settings.LANGUAGES
        return super(LanguageTabsMixin, self).add_view(
            request,
            form_url=form_url,
            extra_context=context
        )
