from modeltranslation.translator import translator, TranslationOptions
from .models import TestPluginModel, TestModel, TestInlineModel


class TestPluginModelTranslationOptions(TranslationOptions):
    fields = ('field1', )


translator.register(TestPluginModel, TestPluginModelTranslationOptions)


class TestModelTranslationOptions(TranslationOptions):
    fields = ('field1', )


translator.register(TestModel, TestModelTranslationOptions)


class TestInlineModelTranslationOptions(TranslationOptions):
    fields = ('field1', )


translator.register(TestInlineModel, TestInlineModelTranslationOptions)
