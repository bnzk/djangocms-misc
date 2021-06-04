import logging
import os
import shutil

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    - copy plugin_template folder to new location
    - search and replace PLUGINTEMPLATE / Plugintemplate / plugintemplate in all files
    - rename template name, test file name
    """
    help = (
        "Bootstrap a new cms based app, providing app hooks and menus extension templates"
        "")

    def add_arguments(self, parser):
        parser.add_argument('path', help="""
The path to copy the files to.
Will take part after last / as package name
""")
        parser.add_argument('app_name', help="""
Name of the new app. CamelCase, as you would name the model: Article/ News / DoorBell.
""")

    def handle(self, *args, **options):
        # Use a stdout logger
        logger = logging.getLogger(__name__)
        stream = logging.StreamHandler(self.stdout)
        logger.addHandler(stream)
        logger.setLevel(logging.DEBUG)

        # copy
        path = options['path']
        app_name = options['app_name']
        current_path = os.path.dirname(__file__)
        source_folder = os.path.join(current_path, '..', '..', 'app_template')
        if not path.startswith('/'):
            target_folder = os.path.join('.', path)
        else:
            target_folder = path
        if os.path.exists(target_folder):
            logger.log(logging.INFO, 'Aborting, target folder already existing: %s' % target_folder)
            return
        shutil.copytree(source_folder, target_folder)

        # replace
        recursive_replace_template(target_folder, 'AppTemplate', app_name)
        recursive_replace_template(target_folder, 'apptemplate', app_name.lower())

        # rename
        base_templates_folder = os.path.join(target_folder, 'templates', )
        templates_folder = os.path.join(base_templates_folder, app_name.lower())
        os.rename(
            os.path.join(base_templates_folder, 'app'),
            templates_folder
        )
        os.rename(
            os.path.join(templates_folder, 'app_list.html'),
            os.path.join(templates_folder, app_name.lower() + '_list.html'),
        )
        os.rename(
            os.path.join(templates_folder, 'app_detail.html'),
            os.path.join(templates_folder, app_name.lower() + '_detail.html'),
        )
        test_folder = os.path.join(target_folder, 'tests', )
        os.rename(
            os.path.join(test_folder, 'app.py'),
            os.path.join(test_folder, 'test_' + app_name.lower() + ".py"),
        )

        logger.log(logging.INFO, 'Success, copied new app files to:')
        logger.log(logging.INFO,  target_folder)
        logger.log(logging.INFO, '---')
        logger.log(logging.INFO, 'Next steps')
        logger.log(logging.INFO, '- Adapt your models.py')
        logger.log(logging.INFO, '- Adapt your views.py (PublishedViewMixin, etc!)')
        logger.log(logging.INFO, '- add your app to INSTALLED_APPS')
        logger.log(logging.INFO, '- run ./manage.py makemigrations')
        logger.log(logging.INFO, '- run ./manage.py test (basic concepts like class names ')
        logger.log(logging.INFO, '  applied, admin form working, adapt to your needs)')


def recursive_replace_template(target_folder, target, replacement):
    for dname, dirs, files in os.walk(target_folder):
        for fname in files:
            if fname[-4:] == '.pyc':
                # nope, dont need em
                continue
            fpath = os.path.join(dname, fname)
            with open(fpath) as f:
                s = f.read()
            s = s.replace(target, replacement)
            with open(fpath, "w") as f:
                f.write(s)
