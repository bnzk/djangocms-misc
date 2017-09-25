from django.conf import settings


def get_env(request):
    """
    expose is_live/stage/dev and SITE_ID to context
    """
    env = getattr(settings, 'ENV', None)
    context = {
        'SITE_ID': settings.SITE_ID,
        'is_live': True if env == 'live' else 0,
        'is_stage': True if env == 'stage' else 0,
        'is_dev': True if env == 'dev' else 0,
    }
    return context
