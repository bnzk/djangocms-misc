from django.urls import path

from .views import AppTemplateListView, AppTemplateDetailView


urlpatterns = [
    path(r'^$', AppTemplateListView.as_view(), name='apptemplate_list'),
    path(r'^detail/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', AppTemplateDetailView.as_view(), name='apptemplate_detail'),
]
