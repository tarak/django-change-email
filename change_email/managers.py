import datetime

from django.db import models

from change_email import app_settings


EMAIL_CHANGE_EXPIRATION_DAYS = getattr(app_settings, 'EMAIL_CHANGE_EXPIRATION_DAYS')


class ExpiredEmailChangeManager(models.Manager):
    def get_query_set(self):
        """Returns all instances that are older than EMAIL_CHANGE_EXPIRATION_DAYS."""
        delta = datetime.timedelta(days=EMAIL_CHANGE_EXPIRATION_DAYS)
        expiration_date = datetime.datetime.now() - delta
        queryset = super(ExpiredEmailChangeManager, self).get_query_set()
        return queryset.filter(date__lte=expiration_date.strftime("%Y-%m-%d %H:%M:%S"))


class PendingEmailChangeManager(models.Manager):
    def get_query_set(self):
        """Returns all instances that are newer than EMAIL_CHANGE_EXPIRATION_DAYS."""
        delta = datetime.timedelta(days=EMAIL_CHANGE_EXPIRATION_DAYS)
        expiration_date = datetime.datetime.now() - delta
        queryset = super(PendingEmailChangeManager, self).get_query_set()
        return queryset.filter(date__gt=expiration_date.strftime("%Y-%m-%d %H:%M:%S"))
