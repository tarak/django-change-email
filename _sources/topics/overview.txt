.. _overview:

========
Overview
========

.. _features:

--------
Features
--------

- Allows users to change the email address in
  :class:`django.contrib.auth.models.User`.
- Allows users to manage pending email address change requests, including
  viewing and deleting pending requests.
- Django's admin integration, see :ref:`api-admin`
- Optional use of the django messages framework

.. _workflow:

--------------------------------------
How email address change requests work
--------------------------------------

There might be the situation where a user wants or needs to change the email
address in :class:`django.contrib.auth.models.User`. Such a request is handled
considering following rules:

- A user is only allowed one change request at a time.
- If a user unintentionally supplied a wrong email address a pending change
  request explicitly needs to be deleted before a new one can be requested. The
  user needs to delete the pending request by him- or herself. This is to
  prevent administrational issues on projects.
