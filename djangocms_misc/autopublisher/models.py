from __future__ import unicode_literals

from cms.models import CMSPlugin
from django.db.models.signals import post_save
from django.dispatch import receiver


def check_publish(title_obj):
    page = title_obj.page
    if title_obj.published:
        if page.publisher_is_draft and title_obj.is_dirty():
            page.publish(title_obj.language)
            print "done publishing!"


@receiver(
    post_save,
    dispatch_uid="cms_autopublisher_publish_check_plugin",
)
def check_publish_plugin(sender, instance, **kwargs):
    if issubclass(sender, CMSPlugin):
        page = instance.placeholder.page
        title = page.get_title_obj(instance.language)
        check_publish(title)


@receiver(
    post_save,
    sender='cms.Title',
    dispatch_uid="cms_autopublisher_publish_check_title",
)
def check_publish_title(sender, instance, **kwargs):
    check_publish(instance)
