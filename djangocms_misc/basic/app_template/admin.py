from cms.admin.placeholderadmin import PlaceholderAdminMixin
from django.contrib import admin

from .models import AppTemplate


@admin.register(AppTemplate)
class AppTemplateAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('date', 'title', 'published', )
    fieldsets = (
        ('', {
            'fields': (
                'published',
                (
                    'title',
                    'seo_title',
                    'date'
                ),
                'meta_description',
                # 'preview_text',
                'preview_image',
            )
        }),
    )
