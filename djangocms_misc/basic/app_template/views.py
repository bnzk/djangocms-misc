from django.views.generic import ListView, DetailView

from .models import AppTemplate
from .views_utils import PublishedViewMixin, AutoSlugMixin, LanguageChooserEnhancerMixin


class AppTemplateListView(PublishedViewMixin, ListView):
    model = AppTemplate


class AppTemplateDetailView(
    AutoSlugMixin,
    PublishedViewMixin,
    LanguageChooserEnhancerMixin,
    DetailView,
):
    model = AppTemplate
