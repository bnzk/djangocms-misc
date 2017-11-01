
from cms.utils import plugins
from .plugins import assign_plugins
from .plugins import move_plugin
from cms.admin.placeholderadmin import PlaceholderAdminMixin

plugins.assign_plugins = assign_plugins
PlaceholderAdminMixin.original_move = PlaceholderAdminMixin.move_plugin
PlaceholderAdminMixin.move_plugin = move_plugin
