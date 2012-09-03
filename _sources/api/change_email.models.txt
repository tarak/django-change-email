.. _api-models:

Models
======

.. automodule:: change_email.models


.. model:: EmailChange

``EmailChange``
---------------

.. autoclass:: change_email.models.EmailChange
   :members:

   .. attribute:: new_email

       Required. The new email address.

   .. attribute:: user

       Required. The :class:`~django.contrib.auth.models.User` that has
       requested the change of email address. Must be set by the view creating
       an email address change request.

   .. attribute:: date

       A :py:obj:`.datetime` of the request's creation. Is set to the current
       date/time upon instance creation.

