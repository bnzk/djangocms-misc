from __future__ import unicode_literals

# from cms.admin.static_placeholder import StaticPlaceholderAdmin
# from django.conf import settings
# from django.urls import resolve
from cms.models import CMSPlugin, StaticPlaceholder
from cms.signals import post_placeholder_operation  # post_obj_operation
from django.db.models.signals import post_save
from django.dispatch import receiver

# ugly
from cms import __version__ as cms_version
CMS_VERSION_36 = cms_version.startswith('3.6.')


def check_publish(title_obj, force_non_dirty=False):
    page = title_obj.page
    if title_obj.published and page.publisher_is_draft:
        # print("published and draft!")
        # print(title_obj.is_dirty())
        # not dirty, after plugin add, in cms 3.6!
        if title_obj.is_dirty() or force_non_dirty or CMS_VERSION_36:
            # print("NEEEEEDs publishing")
            page.publish(title_obj.language)
            # from cms.api import publish_page
            # publish_page(page, user, title_obj.language)
            # print("done publishing")
    else:
        pass


@receiver(
    post_save,
    dispatch_uid="cms_autopublisher_publish_check_save_plugin_instance",
)
def cms_plugin_instance_post_save(sender, instance, **kwargs):
    # print("post save whatever")
    # print(sender)
    created = kwargs.get('created')
    # print(created)
    if created and issubclass(sender, CMSPlugin):
        page = getattr(instance.placeholder, 'page', None)
        if page:
            title = page.get_title_obj(instance.language)
            check_publish(title)


# @receiver(
#     post_delete,
#     dispatch_uid="cms_autopublisher_publish_check_post_delete_plugin_instance",
# )
# def cms_plugin_instance_post_delete(sender, instance, **kwargs):
#     if issubclass(sender, CMSPlugin):
#         page = instance.placeholder.page
#         if page:
#             title = page.get_title_obj(instance.language)
#             check_publish(title)


# ATTENTION ! ***** is called BEFORE page is marked dirty!!!
# works well for move operations, but not perfect for copy paste! (order is not taken)
# source of signals:
@receiver(
    post_placeholder_operation,
    dispatch_uid="cms_autopublisher_post_placeholder_operation",
)
def check_post_placeholder_operation(sender, operation, request, language, token, origin, **kwargs):
    print("post placeholder operation!")
    # print(sender)
    # print(operation)
    # print(request)
    # print(language)
    # print(kwargs)
    # print(origin)
    plugin = None
    placeholder = None
    language = None
    if operation == 'move_plugin':
        plugin = kwargs.get('plugin', None)
    # solved with above post_save signal
    # if operation == 'add_plugin':
    #     plugin = kwargs.get('plugin', None)
    if operation == 'delete_plugin':
        plugin = kwargs.get('plugin', None)
    if operation == 'paste_plugin':
        plugin = kwargs.get('plugin', None)
    if operation == 'change_plugin':
        plugin = kwargs.get('new_plugin', None)
    if operation == 'cut_plugin':
        placeholder = kwargs.get('source_placeholder', None)
        the_plugin = kwargs.get('plugin', None)
        language = the_plugin.language
    if operation == 'paste_placeholder':
        plugin = kwargs.get('plugins', [None, ])[0]
    if operation == 'clear_placeholder':
        plugin = kwargs.get('plugins', [None, ])[0]

    if plugin:
        placeholder = plugin.placeholder
        language = plugin.language
    if placeholder:
        page = getattr(placeholder, 'page', None)
        if page:
            title = page.get_title_obj(language)
            check_publish(title, force_non_dirty=True)
        else:
            if placeholder._get_attached_model() == StaticPlaceholder:
                # print("static placeholder!")
                attached_objs = placeholder._get_attached_objects()
                if len(attached_objs) == 1:
                    attached_objs[0].publish(None, language, force=True)
        return


# # TODO: can Title instances still be deleted? or just be unpublished, what would be covered here?
@receiver(
    post_save,
    sender='cms.Title',
    dispatch_uid="cms_autopublisher_publish_check_save_title",
)
def check_title_post_save(sender, instance, **kwargs):
    # print("cms Title check")
    check_publish(instance)


# @receiver(
#     post_save,
#     sender='cms.Page',
#     dispatch_uid="cms_autopublisher_publish_check_save_title",
# )
# def cms_page_post_save(sender, instance, **kwargs):
#     print "cms Page check. marking as dirty is done on TItle object!"
#     for title in instance.title_set.all():
#         check_publish(title)
