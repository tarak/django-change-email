from django.conf import settings as django_settings

from easysettings import AppSettings


class Settings(AppSettings):
    """
Default settings for django-change-email.
"""
    #: Determines the URL to redirect to after an email change request has been
    #: deleted.
    EMAIL_CHANGE_DELETE_SUCCESS_REDIRECT_URL = '/account/email/change/'
    #: Determines the e-mail address field on the (custom) user model.
    EMAIL_CHANGE_FIELD = 'email'
    #: Determines the e-mail address used to send confirmation mails.
    EMAIL_CHANGE_FROM_EMAIL = django_settings.DEFAULT_FROM_EMAIL
    #: Determines wether to send HTML emails.
    EMAIL_CHANGE_HTML_EMAIL = False
    #: Determines the template used to render the HTML text of the
    #: confirmation email.
    EMAIL_CHANGE_HTML_EMAIL_TEMPLATE = 'change_email/mail/body.html'
    #: Determines the template used to render the subject of the
    #: confirmation email.
    EMAIL_CHANGE_SUBJECT_EMAIL_TEMPLATE = 'change_email/mail/subject.txt'
    #: Determines the expiration time of an e-mail address change requests.
    #: Defaults to 7 days.
    EMAIL_CHANGE_TIMEOUT = 60*60*24*7
    #: Determines the template used to render the plain text body of the
    #: confirmation email.
    EMAIL_CHANGE_TXT_EMAIL_TEMPLATE = 'change_email/mail/body.txt'
    #: Determines wether to use HTTPS when generating the confirmation link.
    EMAIL_CHANGE_USE_HTTPS = False
    #: Determines wether to check if the email address is used on a particular
    #: site. Set to True to make email addresses unique on different sites.
    EMAIL_CHANGE_VALIDATE_SITE = False


settings = Settings()
