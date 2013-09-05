
.. _maintenance:

-----------
Maintenance
-----------

``django-change-email`` provides a maintenance command to delete expired email
address change requests automatically. To do so, simply run the following inside
a project's root directory::

    $ python manage.py cleanupemailchangerequests
