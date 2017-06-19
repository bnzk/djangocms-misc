"""Settings that need to be set in order to run the tests."""
import os, sys
import tempfile
import logging


DEBUG = True

logging.getLogger("factory").setLevel(logging.WARN)

SITE_ID = 1

# from selenium.webdriver.firefox import webdriver
# from selenium.webdriver.phantomjs import webdriver
# SELENIUM_WEBDRIVER = webdriver

APP_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".."))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
    }
}


LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English', ),
    ('de', 'Deutsch', ),
)

ROOT_URLCONF = 'djangocms_misc.tests.urls'

MEDIA_ROOT = os.path.join(APP_ROOT, 'tests/test_app_media')
MEDIA_URL = "/media/"
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(APP_ROOT, '../test_app_static')
STATICFILES_DIRS = (
    os.path.join(APP_ROOT, 'static'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                # 'django.template.loaders.eggs.Loader',
            ],
        }
    },
]

CMS_TEMPLATES = (
    ('base.html', 'Default'),
)

COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(
    os.path.join(APP_ROOT, 'tests/coverage'))
COVERAGE_MODULE_EXCLUDES = [
    'tests$', 'settings$', 'urls$', 'locale$',
    'migrations', 'fixtures', 'admin$', 'django_extensions',
]

EXTERNAL_APPS = (
    # 'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    # cms
    'sekizai',
    'treebeard',
    'cms',
    'djangocms_admin_style',
    'menus',
    'filer',
    'mptt',
    'easy_thumbnails',
    'ckeditor',

    'django.contrib.admin',

)

INTERNAL_APPS = (
    'djangocms_misc.basic',
    'djangocms_misc.admin_style',
    # 'djangocms_misc.apphook_templates',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

INSTALLED_APPS = INTERNAL_APPS + EXTERNAL_APPS
COVERAGE_MODULE_EXCLUDES += EXTERNAL_APPS

SECRET_KEY = 'foobarXXXxxsvXY'
