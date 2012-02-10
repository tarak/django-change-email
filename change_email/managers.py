import datetime

from django.db import models

from change_email import app_settings


EMAIL_CHANGE_VERIFICATION_DAYS = getattr(app_settings, 'EMAIL_CHANGE_VERIFICATION_DAYS')


class ExpiredEmailChangeManager(models.Manager):
    def get_query_set(self):
        """Returns all instances that are older than EMAIL_CHANGE_VERIFICATION_DAYS."""
        delta = datetime.timedelta(days=EMAIL_CHANGE_VERIFICATION_DAYS)
        expiration_date = datetime.datetime.now() - delta
        return super(EmailChangeExpiredManager, self).get_query_set().filter(created__lte=expiration_date.strftime("%Y-%m-%d %H:%M:%S"))
