from __future__ import unicode_literals

from cms.models import CMSPlugin
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


def check_publish(title_obj):
    page = title_obj.page
    if title_obj.published:
        if page.publisher_is_draft and title_obj.is_dirty():
            page.publish(title_obj.language)
            print "done publishing!"


@receiver(
    post_save,
    dispatch_uid="cms_autopublisher_publish_check_save_plugin",
)
def check_publish_plugin_post_save(sender, instance, **kwargs):
    print sender
    print "checker"
    if issubclass(sender, CMSPlugin) or isinstance(sender, CMSPlugin):
        page = instance.placeholder.page
        if page:
            title = page.get_title_obj(instance.language)
            check_publish(title)


@receiver(
    post_delete,
    dispatch_uid="cms_autopublisher_publish_check_post_delete_plugin",
)
def check_publish_plugin_post_delete(sender, instance, **kwargs):
    if issubclass(sender, CMSPlugin):
        print "cms Plugin check"
        page = instance.placeholder.page
        if page:
            title = page.get_title_obj(instance.language)
            check_publish(title)


# TODO: can Title instances still be deleted? or just be unpublished, what would be covered here?
@receiver(
    post_save,
    sender='cms.Title',
    dispatch_uid="cms_autopublisher_publish_check_save_title",
)
def check_publish_title_post_save(sender, instance, **kwargs):
    print "cms Title check"
    check_publish(instance)
