from django.contrib import admin
from modeltranslation.admin import (
    TranslationAdmin,
    TranslationStackedInline,
    TranslationTabularInline,
)

from ...basic.admin import LanguageTabsMixin
from .models import TestInlineModel, TestModel


class TestInlineModelInline(TranslationStackedInline, admin.StackedInline):
    model = TestInlineModel
    extra = 2


class TestInlineModelInline2(TranslationTabularInline, admin.TabularInline):
    model = TestInlineModel
    extra = 2


@admin.register(TestModel)
class TestModelAdmin(LanguageTabsMixin, TranslationAdmin, admin.ModelAdmin):
    inlines = [
        TestInlineModelInline,
        TestInlineModelInline2,
    ]
    fieldsets = [
        [
            "",
            {
                "fields": [
                    "field0",
                ]
            },
        ],
        ["First Set", {"fields": ["field1", "field2"]}],
    ]
