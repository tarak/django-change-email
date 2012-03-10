from django.conf import settings
from django.core.urlresolvers import reverse


EMAIL_CHANGE_EXPIRATION_DAYS = getattr(settings, 'EMAIL_CHANGE_EXPIRATION_DAYS', 7)
EMAIL_CHANGE_FROM_EMAIL = getattr(settings, 'EMAIL_CHANGE_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL)
EMAIL_CHANGE_HTML_EMAIL = getattr(settings, 'EMAIL_CHANGE_HTML_EMAIL', False)
EMAIL_CHANGE_SUBJECT_EMAIL_TEMPLATE = getattr(settings, 'EMAIL_CHANGE_SUBJECT_EMAIL_TEMPLATE', 'change_email/emailchange_subject.txt')
EMAIL_CHANGE_TXT_EMAIL_TEMPLATE = getattr(settings, 'EMAIL_CHANGE_TXT_EMAIL_TEMPLATE', 'change_email/emailchange_email.txt')
EMAIL_CHANGE_HTML_EMAIL_TEMPLATE = getattr(settings, 'EMAIL_CHANGE_HTML_EMAIL_TEMPLATE', 'change_email/emailchange_email.html')

EMAIL_CHANGE_DELETE_SUCCESS_REDIRECT_URL = getattr(settings, 'EMAIL_CHANGE_DELETE_SUCCESS_REDIRECT_URL', '/account/email/change/')
