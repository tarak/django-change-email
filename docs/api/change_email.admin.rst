.. _api-admin:

Admin interface integration
===========================

django-change-email ships a :class:`django.contrib.admin.ModelAdmin` class that
integrates into the Django admin interface and one admin action to manage
pending email address change requests:

.. automodule:: change_email.admin

.. admin:: resend_confirmation

``resend_confirmation``
-----------------------

.. autofunction:: change_email.admin.resend_confirmation

.. admin:: EmailChangeAdmin

``EmailChangeAdmin``
--------------------

.. autoclass:: change_email.admin.EmailChangeAdmin
   :members:
