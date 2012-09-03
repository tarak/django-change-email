.. _api-validators:

Validators
==========

django-change-email provides a validator to check if new email addresses are not
already used by other users or in other pending email address change requests:

.. automodule:: change_email.validators

.. validator:: EmailNotUsedValidator

``EmailNotUsedValidator``
--------------------------

.. autoclass:: change_email.validators.EmailNotUsedValidator
   :members:

.. validator:: validate_email_not_used

``validate_email_not_used``
-----------------------------
.. data:: validate_email_not_used

    An :class:`EmailNotUsedValidator` instance.
