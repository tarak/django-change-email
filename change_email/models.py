import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from change_email import app_settings
from change_email.managers import ExpiredEmailChangeManager


EMAIL_CHANGE_VERIFICATION_DAYS = getattr(app_settings, 'EMAIL_CHANGE_VERIFICATION_DAYS')


class EmailChange(models.Model):
    """
    A model to temporarily store an e-mail adresses change request.

    A new email address is required. Other fields are optional. The user
    relation (OneToOneField) is set automatically upon instance creation.
    """
    new_email = models.EmailField(unique=True, verbose_name=_('new email address'),)
    date = models.DateTimeField(auto_now_add=True, help_text=_('The date and time the email address change was requested.'), verbose_name=_('date'),)
    user = models.OneToOneField(User, help_text=_('The user that has requested the email address change.'), verbose_name=_('user'),)

    objects = models.Manager()
    expired_objects = ExpiredEmailChangeManager()

    class Meta:
        verbose_name = _('email address change request')
        verbose_name_plural = _('email address change requests')
        get_latest_by = "date"

    def __unicode__(self):
        return "%s" % self.user.username

    def get_absolute_url(self):
        return reverse('change_email_detail',  pk=self.pk)

    def has_expired(self):
        "An instance method to determine whether the email address change request has expired."
        delta = datetime.timedelta(days=EMAIL_CHANGE_VERIFICATION_DAYS)
        expiration_date = datetime.datetime.now() - delta
        return expiration_date >= self.created
