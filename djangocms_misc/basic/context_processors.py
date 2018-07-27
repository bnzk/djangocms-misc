from __future__ import unicode_literals
from django.conf import settings


def get_env(request):
    """
    expose is_live/stage/dev and SITE_ID to context
    """
    context = {
        'SITE_ID': settings.SITE_ID,
    }
    env = getattr(settings, 'ENV', None)
    if env:
        context.update({
            'ENV': settings.ENV,
            'is_' + str(env): True,
        })
    return context
