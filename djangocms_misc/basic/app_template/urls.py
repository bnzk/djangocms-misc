from django.urls import path

from .views import AppTemplateDetailView, AppTemplateListView

urlpatterns = [
    path("", AppTemplateListView.as_view(), name="apptemplate_list"),
    path(
        "detail/<int:pk>/<slug:slug>/$",
        AppTemplateDetailView.as_view(),
        name="apptemplate_detail",
    ),
]
