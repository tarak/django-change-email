from django.core.management.base import NoArgsCommand

from change_email.models import EmailChange


class Command(NoArgsCommand):
    help = "Delete expired email change requests from the database"

    def handle_noargs(self, **options):
        EmailChange.expired_objects.delete()
