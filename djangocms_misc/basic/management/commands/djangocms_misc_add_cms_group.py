import logging
import os
import shutil

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db.models import Q


class Command(BaseCommand):
    """
    """
    help = (
        "Add an auth.Group that gives basic CMS Permissions. User --plugin or --cms to add additional perms."
        "")

    def add_arguments(self, parser):
        parser.add_argument(
            '--cms-base',
            required=False,
            action='store_const',
            const=True,
            default=False,
            help="Basic CMS permissions (edit and publish pages, etc).")
        parser.add_argument(
            '--cms-publish',
            required=False,
            action='store_const',
            const=True,
            default=False,
            help="adds exactly 'can publish page' permission)."
        "")
        parser.add_argument(
            '--cms-superuser',
            required=False,
            action='store_const',
            const=True,
            default=False,
            help="Superuser CMS permissions (add own users, page permissions, etc, etc)."
        "")
        parser.add_argument(
            '--plugin',
            required=False,
            action='store_const',
            const=True,
            default=False,
            help="""
Searches for permissions with 'plugin' in their content type's app_label (ex.: cmsplugin_googlemaps), adds to group.""")
        parser.add_argument(
            '--cms',
            action='store_const',
            const=True,
            default=False,
            required=False,
            help="""
Searches for permissions with 'cms' in their content type's app_label (ex.:djangocms_text_ckeditor), adds to group.""")
        parser.add_argument(
            '--name',
            required=False,
            default='cms_base',
            help="""
Name of group. Defaults to cms_base.""")
        parser.add_argument(
            '--force',
            action='store_const',
            const=True,
            required=False,
            help="""
Force overwrite of existing group and it's permissions.""")

    def handle(self, *args, **options):
        group_name = options.get('name')
        # copy
        groups = Group.objects.filter(name=group_name)
        if groups.count():
            if not options.get('force', None):
                exit("use --force to overwrite existing groups!")
            if groups.count() > 1:
                exit("more than one group with name that name ({}) found! exiting.".format(group_name))
            group = groups.first()
        else:
            group = Group.objects.create(name=group_name)

        group.permissions.clear()
        if options.get('cms_base'):
            q_filter = Q(content_type__app_label='cms')
            q_exclude = Q(name__icontains='user')
            q_exclude |= Q(name__icontains='permission')
            q_exclude |= Q(name__icontains='publish')
            self.add_permission(group, q_filter, q_exclude)
        if options.get('cms_publish'):
            q_filter = Q(content_type__app_label='cms')
            q_filter &= Q(name__icontains='publish')
            self.add_permission(group, q_filter)
        if options.get('cms_superuser'):
            q_filter = Q(content_type__app_label='cms')
            self.add_permission(group, q_filter)
        if options.get('cms'):
            q_filter = Q(content_type__app_label__icontains='cms')
            q_exclude = Q(content_type__app_label='cms')
            self.add_permission(group, q_filter, q_exclude)
        if options.get('plugin'):
            q_filter = Q(content_type__app_label__icontains='plugin')
            q_exclude = Q(content_type__app_label='cms')
            self.add_permission(group, q_filter, q_exclude)

        print(logging.INFO, 'Group created! ({})'.format(group_name))
        print(logging.INFO, 'Following permissions were granted:')
        for perm in group.permissions.all():
            print(logging.INFO, '{}'.format(perm))

    def add_permission(self, group, q_filter=Q(), q_exclude=Q()):
        perms = Permission.objects.filter(q_filter).exclude(q_exclude)
        group.permissions.add(*perms)
