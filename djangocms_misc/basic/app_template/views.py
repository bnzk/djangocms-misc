from django.views.generic import DetailView, ListView

from .models import AppTemplate
from .views_utils import AutoSlugMixin, LanguageChooserEnhancerMixin, PublishedViewMixin


class AppTemplateListView(PublishedViewMixin, ListView):
    model = AppTemplate


class AppTemplateDetailView(
    AutoSlugMixin,
    PublishedViewMixin,
    LanguageChooserEnhancerMixin,
    DetailView,
):
    model = AppTemplate
