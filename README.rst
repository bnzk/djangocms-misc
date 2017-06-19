djangocms-misc
===============

.. image:: https://travis-ci.org/bnzk/djangocms-misc.svg
    :target: https://travis-ci.org/bnzk/djangocms-misc/
.. image:: https://img.shields.io/pypi/v/djangocms-misc.svg
    :target: https://pypi.python.org/pypi/djangocms-misc/
.. image:: https://img.shields.io/pypi/l/djangocms-misc.svg
    :target: https://pypi.python.org/pypi/djangocms-misc/

customizing django / django-cms, as a set of diferent apps, that can be installed individually


Features
--------

**Implemented**

- djangocms_misc.admin_style
  - better change view styles for djangocms-admin-style (visible fieldsets/inlines/etc)
  - other minor admin enhancements for djangocms-admin-style
- djangocms_misc.usability
  - hide "create" button in toolbar, with css
  - other opiniated things, that you might not want
- djangocms_misc.tags
  - convenience page_link tag: {% page_link "reverse_id_or_the_like" "css_class_name" "custom_link_text" %}
  - helper tag for getting images from image fields in plugins/placeholders. useful for fb:og tags and the like

**Yet to be done**

- djangocms_misc.apphook_templates
  - somehow link app_hook and template together (make apphook selectable via template -> magic [signals])
  - needs proofe of concept
- management commands
  - other?


Installation & Usage
--------------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install djangocms-misc

Add needed ``djangocms-misc`` subapps to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'djangocms_misc.basic',  # tags, cms frontend enhances
        'djangocms_misc.admin_style',  # djangocms-admin-style enhanced
        'djangocms_misc.apphook_templates',  # experimental, not implemented
    )

Basic
*****

**Pagelink tag**, looks for page, displays nothing if nothing found.

.. code-block:: django

    {% load djangocms_misc_tags %}
    {% djangocms_misc_page_link 'contact' %}

**CMS Frontend style**, very small adaptions, plus removing the "create" button in the toolbar. You must include
the following stylesheet in your main html template.

.. code-block:: django

    <link rel="stylesheet" href="{{ STATIC_URL }}djangocms_misc/css/cms_frontend_adjust.css">


Admin Style
***********

Install this subapp to have a slightly optimized/opiniated djangocms-admin-style version. No further action needed.


Apphook Templates
*****************

Experimental, not developed yet.


Development
-----------

No testsuite yet!

- there is test app, available with `./manage.py runserver`.
- to run tests: ./manage.py test
- to run tests with django 1.8 / 1.9 / 1.10 / 1.11: `tox`


Contributions
-------------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

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
