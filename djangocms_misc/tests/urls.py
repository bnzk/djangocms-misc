"""URLs to run the tests."""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views import static


admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
    ]
