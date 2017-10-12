
from cms.utils import plugins
from .plugins import assign_plugins


setattr(plugins, 'assign_plugins', assign_plugins)
