"""
These settings are used by the ``manage.py`` command.

"""
from .settings_test import *  # NOQA


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
    }
}
