from django.contrib import admin

from .models import TestModel, TestInlineModel


class TestInlineModelInline(admin.StackedInline):
    model = TestInlineModel
    extra = 2


class TestInlineModelInline2(admin.TabularInline):
    model = TestInlineModel
    extra = 2


class TestModelAdmin(admin.ModelAdmin):
    inlines = [TestInlineModelInline, TestInlineModelInline2, ]
    fieldsets = [
        ['', {'fields': ['field0', ]}],
        ['First Set', {'fields': ['field1', 'field2']}],
    ]


admin.site.register(TestModel, TestModelAdmin)
