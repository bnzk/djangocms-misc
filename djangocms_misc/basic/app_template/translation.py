from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import AppTemplate


@register(AppTemplate)
class AppTemplateTranslationOptions(TranslationOptions):
    fields = [
        "title",
    ]
