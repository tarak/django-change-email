import datetime

from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


from change_email import app_settings
from change_email.managers import ExpiredEmailChangeManager
from change_email.managers import PendingEmailChangeManager
from change_email.tokens import default_token_generator


EMAIL_CHANGE_FROM_EMAIL = getattr(app_settings, 'EMAIL_CHANGE_FROM_EMAIL')
EMAIL_CHANGE_HTML_EMAIL = getattr(app_settings, 'EMAIL_CHANGE_HTML_EMAIL')
EMAIL_CHANGE_HTML_EMAIL_TEMPLATE = getattr(app_settings, 'EMAIL_CHANGE_HTML_EMAIL_TEMPLATE')
EMAIL_CHANGE_SUBJECT_EMAIL_TEMPLATE = getattr(app_settings, 'EMAIL_CHANGE_SUBJECT_EMAIL_TEMPLATE')
EMAIL_CHANGE_TXT_EMAIL_TEMPLATE = getattr(app_settings, 'EMAIL_CHANGE_TXT_EMAIL_TEMPLATE')
EMAIL_CHANGE_EXPIRATION_DAYS = getattr(app_settings, 'EMAIL_CHANGE_EXPIRATION_DAYS')


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
    pending_objects = PendingEmailChangeManager()

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
        delta = datetime.timedelta(days=EMAIL_CHANGE_EXPIRATION_DAYS)
        expiration_date = datetime.datetime.now() - delta
        return expiration_date >= self.date

    def send_confirmation_mail(self):
        """An instance method to send a confirmation mail to the new email address.

The confirmation email will make use of three templates that
can be set in each project's settings:

:template:`change_email/emailchange_subject.txt`
    This template will be used for the subject line of the
    email. Because it is used as the subject line of an email,
    this template's output **must** be only a single line of
    text; output longer than one line will be forcibly joined
    into only a single line.


:template:`change_email/emailchange_email.txt`
    This template will be used for the body of the email.

:template:`change_email/emailchange_email.html`
    This template will be used for the HTML part of the email.

These templates will each receive the following context
variables:

``date``
    The date when this email address change was requested.

``expiration_days``
    The number of days remaining during which this request may
    be waiting for confirmation.

``current_site``
    An object representing the current site on which the user
    is logged in.  Depending on whether ``django.contrib.sites``
    is installed, this may be an instance of either
    ``django.contrib.sites.models.Site`` (if the sites
    application is installed) or
    ``django.contrib.sites.models.RequestSite`` (if
    not).Consult the documentation for the Django sites
    framework for details regarding these objects' interfaces.

``new_email``
    The new email address.

``token``
    The confirmation token for the new email address.

``user``
    The user that has requested this email address change.

        """
        if Site._meta.installed:
            current_site = Site.objects.get_current()
        else:
            current_site = RequestSite(request)
        token = default_token_generator.make_token(self.user)
        ctx_dict = {'current_site': current_site,
                    'date': self.date,
                    'expiration_days': EMAIL_CHANGE_EXPIRATION_DAYS,
                    'new_email': self.new_email,
                    'token': token,
                    'user': self.user,}
        subject = render_to_string(EMAIL_CHANGE_SUBJECT_EMAIL_TEMPLATE,
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        text_message = render_to_string(EMAIL_CHANGE_TXT_EMAIL_TEMPLATE,
                                   ctx_dict)
        if EMAIL_CHANGE_HTML_EMAIL:
            html_message = render_to_string(EMAIL_CHANGE_HTML_EMAIL_TEMPLATE,
                                   ctx_dict)
            msg = EmailMultiAlternatives(subject, text_message, EMAIL_CHANGE_FROM_EMAIL, [self.new_email])
            msg.attach_alternative(html_message, "text/html")
            msg.send()
        else:
            send_mail(subject, text_message, EMAIL_CHANGE_FROM_EMAIL, [self.new_email])
