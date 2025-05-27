from django.apps import AppConfig


class EUTAppConfig(AppConfig):
    name = "djangocms_misc.editmode_fallback_placeholder"

    def ready(self):
        from cms.admin.placeholderadmin import PlaceholderAdminMixin
        from cms.utils import plugins

        from .plugins import assign_plugins, move_plugin

        plugins.assign_plugins = assign_plugins
        PlaceholderAdminMixin.original_move = PlaceholderAdminMixin.move_plugin
        PlaceholderAdminMixin.move_plugin = move_plugin
