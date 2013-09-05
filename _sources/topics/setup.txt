.. _setup:

==========================
Setting up the application
==========================


.. _setup-templates:

Required templates
==================

To use :ref:`the views in django-change-email <api-views>` several templates
need to be provided.

.. note::
  Because ``django-change-email`` is intended to be highly reusable it does not
  include any other templates than the ones used for testing the application. It
  is left to programmers using ``django-change-email`` to create templates for
  projects as needed.

The naming of these templates follows the convention used
by class based views in Dango:

* ``change_mail/emailchange_confirm.html``
    Used in the view :view:`EmailChangeConfirmView`.
* ``change_mail/emailchange_form.html``
    Used in the view :view:`EmailChangeCreateView`.
* ``change_mail/emailchange_confirm_delete.html``
    Used in the view :view:`EmailChangeDeleteView`.
* ``change_mail/emailchange_detail.html``
    Used in the view :view:`EmailChangeDetailView`.

It is possible to use different templates. Informations on how to change
the templates locations can be found in the :ref:`settings <api-settings>`
documentation.

Additional templates are required to send confirmation mails on email address
change requests. Information on these templates can also be found in the
:ref:`settings <api-settings>` documentation.

.. note::
  Minimal example e-mail templates can be found inside the tests module of
  ``django-change-email``.

.. _setup-urls:

Setting up URLs
===============

``django-change-email`` includes a Django ``URLconf`` which sets up URL patterns
for :ref:`the views in django-change-email <api-views>`. This ``URLconf`` can be
found at ``change_email.urls``, and so can simply be included in a project's
root URL configuration. For example, to place the URLs under the prefix
``/account/``, one could add the following to a project's root ``URLconf``::

    (r'^account/', include('change_email.urls')),

Users would then be able to change their email address or check pending change
requests by visiting the URL ``/account/email/change/``.

.. _setup-add-to-apps:

Adding the app to the installed applications
============================================

To use ``django-change-email`` in a Django project add ``change_email`` to the
``INSTALLED_APPS`` setting of a project.

For example, one might have something like the following in a Django settings
file::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.admin',
        'django.contrib.messages',
        'change_email',
        # ...other installed applications...
    )

.. _setup-create-db-tables:

Creating the database tables
============================

To create the database tables needed by ``django-change-email`` simply run
the following inside a project's root directory::

    $ python manage.py syncdb

