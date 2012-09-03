.. _api-signals:

Signals
=======


django-change-email provides three :class:`django.dispatch.Signal` classes:

.. signal:: email_change_confirmed

``email_change_confirmed``
--------------------------

A signal that is sent when an email address change request is confirmed. Receives
a Request object as single providing argument.

.. signal:: email_change_created

``email_change_created``
------------------------

A signal that is sent when an email address change request is created. Receives a
Request object as single providing argument.

.. signal:: email_change_deleted

``email_change_deleted``
------------------------

A signal that is sent when an email address change request is deleted. Receives a
Request object as single providing argument.
