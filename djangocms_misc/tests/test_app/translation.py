from modeltranslation.translator import TranslationOptions, translator

from .models import TestInlineModel, TestModel, TestPluginModel


class TestPluginModelTranslationOptions(TranslationOptions):
    fields = ("field1",)


translator.register(TestPluginModel, TestPluginModelTranslationOptions)


class TestModelTranslationOptions(TranslationOptions):
    fields = ("field1",)


translator.register(TestModel, TestModelTranslationOptions)


class TestInlineModelTranslationOptions(TranslationOptions):
    fields = ("field1",)


translator.register(TestInlineModel, TestInlineModelTranslationOptions)
