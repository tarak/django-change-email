.. _api-managers:

Managers
========

django-change-email provides two :class:`django.db.models.Manager` classes that
return commonly used querysets.

These managers are used in the :model:`EmailChange` model::

    class EmailChange(models.Model):
        
        ...
        
        objects = models.Manager()
        expired_objects = ExpiredEmailChangeManager()
        pending_objects = PendingEmailChangeManager()

.. automodule:: change_email.managers

.. manager:: ExpiredEmailChangeManager

``ExpiredEmailChangeManager``
-----------------------------

.. autoclass:: change_email.managers.ExpiredEmailChangeManager
   :members:

.. manager:: PendingEmailChangeManager

``PendingEmailChangeManager``
-----------------------------

.. autoclass:: change_email.managers.PendingEmailChangeManager
   :members:
