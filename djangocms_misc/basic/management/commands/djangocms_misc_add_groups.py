import logging
import os
import shutil

from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models import Q


class Command(BaseCommand):
    """
    """
    help = (
        "Add an basic set of auth.Groups for cms usage (cms-base, cms-publisher, cms-superuser, plugin-permissions)  that gives basic CMS Permissions. User --plugin or --cms to add additional perms."
        "")

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_const',
            const=True,
            required=False,
            help="""
        Force overwrite of existing group and it's permissions.""")

    def handle(self, *args, **options):
        args = []
        if options.get('force'):
            args = ['--force', ]
        call_command('djangocms_misc_add_cms_group', '--cms-base', *args)
        call_command('djangocms_misc_add_cms_group', '--cms-publish', '--name=cms_publisher', *args)
        call_command('djangocms_misc_add_cms_group', '--cms-superuser', '--name=cms_superuser', *args)
        call_command('djangocms_misc_add_cms_group', '--cms', '--plugin', '--name=cms_plugin_permissions', *args)
