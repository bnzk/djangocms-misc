from django.forms import widgets


class FormFieldStashMixin(object):

    def formfield_for_dbfield(self, db_field, *args, **kwargs):
        field = super(FormFieldStashMixin, self).formfield_for_dbfield(db_field, *args, **kwargs)
        if getattr(self, 'single_formfield_stash', None):
            for stash_field in self.single_formfield_stash:
                if db_field.name == stash_field:
                    field.widget.attrs['data-formfield-stash'] = "true"
                    field.widget.attrs['data-original-field'] = db_field.name
        if getattr(self, 'formfield_stash', None):
            for stash_field, fields in self.formfield_stash.items():
                if db_field.name == stash_field:
                    field.widget.attrs['data-formfield-stash'] = "true"
                    field.widget.attrs['data-original-field'] = db_field.name
                    for choice, show_fields in fields.items():
                        field.widget.attrs['data-formfield-stash-%s' % choice] = (
                            ','.join(show_fields)
                        )
        return field

    def save_model(self, request, obj, form, change):
        # TODO: implement? design decision! do it on the model!?
        if getattr(self, 'single_formfield_stash', None):
            for stash_field in self.single_formfield_stash:
                for choice, display_choice in form.fields[stash_field].choices:
                    pass
        super(FormFieldStashMixin, self).save_model(request, obj, form, change)

    @property
    def media(self):
        js = (
            'formfield_stash/formfield_stash.js',
        )
        css = {
            'all': ('formfield_stash/adjust-divers.css', ),
        }
        original_media = super(FormFieldStashMixin, self).media
        return original_media + widgets.Media(css=css, js=js)
