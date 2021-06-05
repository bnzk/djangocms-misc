from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from .models import AppTemplate


@register(AppTemplate)
class AppTemplateTranslationOptions(TranslationOptions):
    fields = ['title', ]
