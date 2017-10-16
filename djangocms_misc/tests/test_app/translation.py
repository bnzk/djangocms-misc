from modeltranslation.translator import translator, TranslationOptions
from .models import TestPluginModel


class TestPluginModelTranslationOptions(TranslationOptions):
    fields = ('field1', )


translator.register(TestPluginModel, TestPluginModelTranslationOptions)
