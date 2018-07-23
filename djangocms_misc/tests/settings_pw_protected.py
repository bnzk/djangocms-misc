from .settings import *  # noqa


MIDDLEWARE_CLASSES += ['djangocms_misc.basic.middleware.PasswordProtectedMiddleware', ]  # noqa
