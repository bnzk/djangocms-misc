# djangocms-misc

[![Build Status](https://travis-ci.org/bnzk/djangocms-misc.svg "Build Status")](https://travis-ci.org/bnzk/djangocms-misc/)
[![PyPi Version](https://img.shields.io/pypi/v/djangocms-misc.svg "PyPi Version")](https://pypi.python.org/pypi/djangocms-misc/)
[![Licence](https://img.shields.io/pypi/l/djangocms-misc.svg "Licence")](https://pypi.python.org/pypi/djangocms-misc/)

customizing [django-cms](https://github.com/divio/django-cms), as a set of diferent apps, that can be installed individually


## Features

- [djangocms_misc.basic](#basic)
  - Frontend: Hide CMS's "create" button in toolbar, make structure mode lightly transparent
  - page_link tag: {% page_link "reverse_id_or_the_like" "css_class_name" "custom_link_text" %}
  - helper tag for getting images from image fields in plugins/placeholders.
  useful for fb:og tags and the like.
  - Bot404Middleware, to keep away bots from staging systems
  - get_env context processor, to always have env (stage/live) and current SITE_ID
- [djangocms_misc.admin_style](#admin-style)
  - better change view styles for djangocms-admin-style (visible fieldsets/inlines/etc)
  - other minor admin enhancements for djangocms-admin-style
- [djangocms_misc.global_untranslated_placeholder](#global-untranslated-placeholder)
  - WARNING: experimental
  - monkey patch the cms's `cms.plugin_rendering.ContentRenderer` to one language only, always.
  - simple monkey patch, but side effects still need to be checked out (haystack / aldryn_search?!)
- [djangocms_misc.autopublisher](#autopublisher)
  - WARNING: experimental
  - cheat the cms, so that you'll never have a difference between draft und published version, as every change is
  always published automatically (experimental, for plugins and pages for now, but probably all we need).
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

**Pagelink tag**, looks for page, displays nothing if nothing found.

    {% load djangocms_misc_tags %}
    {% djangocms_misc_page_link 'contact' %}

**CMS Frontend style**, very small adaptions, plus removing the "create" button in the toolbar. You must include
the following stylesheet in your main html template.

    <link rel="stylesheet" href="{{ STATIC_URL }}djangocms_misc/css/cms_frontend_adjust.css">

**Bot404Middleware**, raises a 404 for bots, if enabled. Requires django-user_agents.

Add

    'djangocms_misc.basic.middleware.Bot404Middleware'

to your `settings.MIDDLEWARE` (old style `MIDDLEWARE_CLASSES` should still work). To really enable
it, you need to explicitly set `settings.DJANGOCMS_MISC_BOT404 = True`.

**get_env contect processor**, add SITE_ID and if available, is_live/stage/dev/whatever to the context.

Add

    'djangocms_misc.basic.context_processors.get_env'

to your `settings.TEMPLATES`s context processors. If `settings.ENV = 'live'`, your context will
have `is_live` set to true.

### Admin Style

Add `djangocms_misc.admin_style` to `INSTALLED_APPS` to have a slightly optimized/opiniated djangocms-admin-style version. No further action needed.


### Global Untranslated Placeholder

WARNING: experimental. Get real untranslated placeholders, that have the same plugins,
for all languages. monkey patch `cms.plugin_rendering.ContentRenderer`, to one language only,
always. Very simple patch.

usage: add `djangocms_misc.gloabl_untranslated_placeholder` to `INSTALLED_APPS`. In your settings,
 add `DJANGOCMS_MISC_UNTRANSLATED_PLACEHOLDERS = True` or ` = 'lang_code'`, `True` would default
 to your settings `LANGUAGE_CODE`. This is then the language your plugins will be filled in and
 rendered.

Yet implemented on `develop` branch only!


### Autopublisher

WARNING: very experimental. Goal: Make the "Publish Page changes" non existent, so draft and live
 version are always the same. With every change made in content or pages, publish the page(s)
 automagically. Using cms signals, this is more or less implemented, but still heavily experimental.

usage: add `djangocms_misc.autopublisher` to `INSTALLED_APPS`. Due to when exactly some singals are
called, you must add the following stylesheet, to hide the publish button with css:

    <link rel="stylesheet" href="{{ STATIC_URL }}autopublisher/css/autopublisher.css">

Yet implemented on `develop` branch only!


### Untranslated Placeholder (not under development currently!)

WARNING: very experimental. Would allow mixed translated/untranslated placeholders. Get real untranslated placeholders, that have the same plugins,
for all languages. monkey patch `cms.utils.plugins.assign_plugins`, and due to "different trees",
other monkey patches may be needed (sorting/structure mode!). Currently trying different
approaches, that can be tried: `djangocms_misc.editmode_fallback_placeholder` (always displaying
fallbacks) or `djangocms_misc.untranslated_placeholder` (kind a "real" untranslated placeholder).

usage: add on of the mentioned apps to `INSTALLED_APPS`. In your placeholder settings, either add
`editmode_language_fallback: True` or `untranslated: True`, depending which version you have
installed. There you go.

Yet implemented on `develop` branch only!


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
