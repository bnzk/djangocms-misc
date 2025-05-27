from .settings import *  # noqa


MIDDLEWARE += [  # noqa
    "djangocms_misc.basic.middleware.PasswordProtectedMiddleware",
]
