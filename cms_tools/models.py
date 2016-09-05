from cms.models import CMSPlugin
from django.db import models


class CMSToolsPluginBaseModel(models.Model):
    style = models.CharField(max_length=31, blank=True, default='')
    anchor = models.CharField(max_length=127, blank=True, default='')
    hide = models.BooleanField(default=False)

    class Meta:
        abstract = True