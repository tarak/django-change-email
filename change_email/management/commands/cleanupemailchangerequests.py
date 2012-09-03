from django.core.management.base import NoArgsCommand

from change_email.models import EmailChange


class Command(NoArgsCommand):
    """
The ``cleanupemailchangerequests`` command deletes expired email
address change requests from the database.

Usage::

    $ python manage.py cleanupemailchangerequests
"""
    help = "Delete expired email change requests from the database"

    def handle_noargs(self, **options):
        EmailChange.expired_objects.all().delete()
