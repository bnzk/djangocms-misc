# djangocms-misc

[![Build Status](https://travis-ci.org/bnzk/djangocms-misc.svg "Build Status")](https://travis-ci.org/bnzk/djangocms-misc/)
[![PyPi Version](https://img.shields.io/pypi/v/djangocms-misc.svg "PyPi Version")](https://pypi.python.org/pypi/djangocms-misc/)
[![Licence](https://img.shields.io/pypi/l/djangocms-misc.svg "Licence")](https://pypi.python.org/pypi/djangocms-misc/)

customizing [django-cms](https://github.com/divio/django-cms), as a set of diferent apps, that can be installed individually


## Features

- [djangocms_misc.basic](#basic) (various tools and helpers)
- [djangocms_misc.admin_style](#admin-style) (enhancements for djangocms-admin-style)
- [djangocms_misc.alternate_toolbar](#alternate-toolbar) (alternate djangocms toolbar)
- [djangocms_misc.global_untranslated_placeholder](#global-untranslated-placeholder) (as it says)
- [djangocms_misc.autopublisher](#autopublisher) (draft and live always in sync)
- djangocms_misc.editmode_fallback_placeholder / djangocms_misc.untranslated_placeholder
  - WARNING: only testing, currently following the `global_untranslated_placeholder` approach.
  - WARNING: very experimental
  - would allow mixed translated / untranslated placeholders
  - monkey patch `cms.utils.plugins.assign_plugins` to get untranslated placeholders
  - due to "different trees", other monkey patches may be needed (sorting/copy pasting!)


**Yet to be done/explored**

- djangocms_misc.apphook_templates
  - somehow link app_hook and template together (make apphook selectable via template -> magic [signals])
  - needs proofe of concept
- management commands (?!)


## Installation & Usage

To get the latest stable release from PyPi

    pip install djangocms-misc

Add needed ``djangocms-misc`` subapps to your ``INSTALLED_APPS``

    INSTALLED_APPS = (
        ...,
        'djangocms_misc.basic',  # tags, cms frontend enhances
        'djangocms_misc.admin_style',  # djangocms-admin-style enhanced
        'djangocms_misc.apphook_templates',  # experimental, not implemented
    )



### Basic

- Frontend: Hide CMS's "create" button in toolbar, make structure mode lightly transparent
- page_link tag: {% page_link "reverse_id_or_the_like" "css_class_name" "custom_link_text" %}
- helper tag for getting images from image fields in plugins/placeholders.
useful for fb:og tags and the like.
- RedirectFirstSubpageMiddleware, convenient redirect to first subpages.
- PasswordProtectedMiddleware, to keep away bots from staging systems
- Bot404Middleware, to keep away bots from staging systems
- get_env context processor, to always have env (stage/live) and current SITE_ID

**Pagelink tag**, looks for page, displays nothing if nothing found.

    {% load djangocms_misc_tags %}
    {% djangocms_misc_page_link 'contact' %}

**CMS Frontend style**, very small adaptions, plus removing the "create" button in the toolbar. You must include
the following stylesheet in your main html template.

    <link rel="stylesheet" href="{{ STATIC_URL }}djangocms_misc/css/cms_frontend_adjust.css">

**get_env contect processor**, add SITE_ID and if available, is_live/stage/dev/whatever to the context.

Add

    'djangocms_misc.basic.context_processors.get_env'

to your `settings.TEMPLATES`s context processors. If `settings.ENV = 'live'`, your context will
have `is_live` set to true.


**RedirectFirstSubpageMiddleware**, allows to automagically redirect to a pages first subpage, only if and when, the
redirect field is filled with `/firstchild`.

Add

    'djangocms_misc.basic.middleware.RedirectFirstSubpageMiddleware'

to your `settings.MIDDLEWARE`. A small change to the `menu/menu.html` template is needed, check 
https://github.com/bnzk/djangocms-misc/tree/develop/djangocms_misc/basic/templates/menu/menu.html
(in fact, only check if the redirect is actually `/firstchild`). To make this work, `djangocms_misc.basic` must be 
before `cms`, in `INSTALLED_APPS`. Also, check your own menu templates, if you have.


**PasswordProtectedMiddleware**, only allows authenticated users to access your site - you'll first need to enter valid
credentials at the django admin login screen (normally /admin/login/ )

Add

    'djangocms_misc.basic.middleware.PasswordProtectedMiddleware'

to your `settings.MIDDLEWARE` (old style `MIDDLEWARE_CLASSES` should still work).

**Bot404Middleware**, raises a 404 for bots, if enabled. Requires django-user_agents. No more recommended, better 
use password protected middleware.

Add

    'djangocms_misc.basic.middleware.Bot404Middleware'

to your `settings.MIDDLEWARE` (old style `MIDDLEWARE_CLASSES` should still work). To really enable
it, you need to explicitly set `settings.DJANGOCMS_MISC_BOT404 = True`.



### Admin Style

- better change view styles for djangocms-admin-style (visible fieldsets/inlines/etc)
- other minor admin enhancements/bugfixes for djangocms-admin-style

Add `djangocms_misc.admin_style` to `INSTALLED_APPS`, before `djangocms_admin_style`, to have a slightly optimized/opiniated djangocms-admin-style
version. No further action needed.



### Alternate Toolbar

Other structure for the main CMS toolbar.

- User
  - Change password, user settings, logout
- Administration
  - Pages, Files, Whatever, ...
- Page
  - you know this one
- Language
  - as is
- Clipboard
  - more visible

Add `djangocms_misc.alternate_toolbar` to `INSTALLED_APPS`, and you'll have it as is.
If you want custom items in your administration menu, create your own `cms_toolbars.py`, as follows:

    from django.utils.translation import ugettext_lazy as _
    from cms.toolbar_pool import toolbar_pool
    from cms.utils.urlutils import admin_reverse
    from djangocms_misc.alternate_toolbar.cms_toolbars import AlternateBasicToolbar


    toolbar_pool.unregister(AlternateBasicToolbar)

    @toolbar_pool.register
    class CustomToolbar(AlternateBasicToolbar):

        def add_more_admin_menu_items(self):
            self.admin_menu.add_sideframe_item(
                _('Aktuelles'),
                url=admin_reverse('esb_site_aktuellesartikelmodel_changelist')
            )
            self.admin_menu.add_sideframe_item(
                _('Medienartikel'),
                url=admin_reverse('esb_site_medienbacklinkmodel_changelist')
            )
            advanced_menu = self.admin_menu.get_or_create_menu("advanced", "Erweitert")
            advanced_menu.add_sideframe_item(
                _('Metanavigation'),
                url=admin_reverse('esb_site_metanavigationlinkmodel_changelist')
            )



### Global Untranslated Placeholder

- WARNING: experimental

Get real untranslated placeholders, that have the same plugins,
for all languages. monkey patch `cms.plugin_rendering.ContentRenderer`, to one language only,
always. Very simple patch, but side effects still need to be checked out (haystack / aldryn_search seems ok?!)

usage: add `djangocms_misc.gloabl_untranslated_placeholder` to `INSTALLED_APPS`. In your settings,
 add `DJANGOCMS_MISC_UNTRANSLATED_PLACEHOLDERS = True` or ` = 'lang_code'`, `True` would default
 to your settings `LANGUAGE_CODE`. This is then the language your plugins will be filled in and
 rendered.


### Autopublisher

- WARNING: experimental

Goal: Make the "Publish Page changes" button non existent, so draft and live
 version are always the same. With every change made in content or pages, publish the page(s)
 automagically. Using cms signals, this is more or less implemented, but still heavily experimental.

usage: add `djangocms_misc.autopublisher` to `INSTALLED_APPS`. Due to when exactly some singals are
called, you must add the following stylesheet, to hide the publish button with css:

    <link rel="stylesheet" href="{{ STATIC_URL }}autopublisher/css/autopublisher.css">


### Untranslated Placeholder (not under development currently!)

WARNING: very experimental. Would allow mixed translated/untranslated placeholders. Get real untranslated placeholders, that have the same plugins,
for all languages. monkey patch `cms.utils.plugins.assign_plugins`, and due to "different trees",
other monkey patches may be needed (sorting/structure mode!). Currently trying different
approaches, that can be tried: `djangocms_misc.editmode_fallback_placeholder` (always displaying
fallbacks) or `djangocms_misc.untranslated_placeholder` (kind a "real" untranslated placeholder).

usage: add on of the mentioned apps to `INSTALLED_APPS`. In your placeholder settings, either add
`editmode_language_fallback: True` or `untranslated: True`, depending which version you have
installed. There you go.


## Development


### Getting started

WARNING: No testsuite yet!

- there is test app, available with `./manage.py runserver`.
- to run tests: ./manage.py test
- to run tests with django 1.8 / 1.9 / 1.10 / 1.11: `tox`


### Contributions

If you want to contribute to this project, please perform the following steps

    # Fork this repository
    # Clone your fork
    mkvirtualenv djangocms-misc
    pip install -r test_requirements.txt
    git checkout -b feature_branch
    # Implement your feature and tests
    git add . && git commit
    tox
    git push -u origin feature_branch
    # Send us a pull request for your feature branch
