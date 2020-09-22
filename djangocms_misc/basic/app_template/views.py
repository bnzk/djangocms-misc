from django.views.generic import ListView, DetailView

from .models import AppTemplate
from yourcustomapp.views import PublishedViewMixin, AutoSlugMixin


class AppTemplateListView(PublishedViewMixin, ListView):
    model = AppTemplate


class AppTemplateDetailView(AutoSlugMixin, PublishedViewMixin, DetailView):
    model = AppTemplate
