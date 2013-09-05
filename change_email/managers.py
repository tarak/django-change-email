import datetime

from django.db import models

from change_email.conf import settings


class ExpiredEmailChangeManager(models.Manager):
    def get_query_set(self):
        """
Returns all instances that are older
than :py:attr:`~password_policies.conf.Settings.EMAIL_CHANGE_TIMEOUT`.
"""
        delta = datetime.timedelta(seconds=settings.EMAIL_CHANGE_TIMEOUT)
        expiration_date = datetime.datetime.now() - delta
        queryset = super(ExpiredEmailChangeManager, self).get_query_set()
        date = expiration_date.strftime("%Y-%m-%d %H:%M:%S")
        return queryset.filter(date__lte=date)


class PendingEmailChangeManager(models.Manager):
    def get_query_set(self):
        """
Returns all instances that are newer
than :py:attr:`~password_policies.conf.Settings.EMAIL_CHANGE_TIMEOUT`.
"""
        delta = datetime.timedelta(seconds=settings.EMAIL_CHANGE_TIMEOUT)
        expiration_date = datetime.datetime.now() - delta
        queryset = super(PendingEmailChangeManager, self).get_query_set()
        date = expiration_date.strftime("%Y-%m-%d %H:%M:%S")
        return queryset.filter(date__gt=date)
