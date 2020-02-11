"""URLs to run the tests."""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views import static


admin.autodiscover()

urlpatterns = [
]

urlpatterns += i18n_patterns(
    url(r'^admin/', admin.site.urls),
    url(r'^', include('cms.urls')),
)


if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
    ]
