# django-cms-tools

customizing django / django-cms, as a set of contrib apps, that can be installed individually

## planned

- djangocms_tools.admin_style
  - better change view styles for djangocms-admin-style (visible fieldsets/inlines/etc)
  - other minor admin enhancements for djangocms-admin-style
- djangocms_tools.usability
  - hide "create" button in toolbar, with css
  - other opiniated things, that you might not want
- djangocms_tools.tags
  - convenience page_link tag: {% page_link "reverse_id_or_the_like" "css_class_name" "custom_link_text" %}
  - helper tag for getting images from image fields in plugins/placeholders. useful for fb:og tags and the like
- djangocms_tools.apphook_templates
  - somehow link app_hook and template together (make apphook selectable via template -> magic [signals])
  - needs proofe of concept
- management commands
  - wipe filer thumbnails folder
  - remove orphaned filer files?!
  - other?
