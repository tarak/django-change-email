from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from change_email.conf import settings
from change_email.models import EmailChange


class EmailNotUsedValidator(object):
    """
A validator to check if a given email address is already taken.
"""
    code = "email_in_use"
    msg = _("This email address is already in use."
            " Please supply a different email address.")

    def __call__(self, value):
        UserModel = get_user_model()
        key = '%s__iexact' % settings.EMAIL_CHANGE_FIELD
        kwargs = {key: value}
        if settings.EMAIL_CHANGE_VALIDATE_SITE:
            site = Site.objects.get_current()
            kwargs['site'] = site
        if UserModel.objects.filter(**kwargs).count():
            raise ValidationError(self.msg, code=self.code)
            return
        del kwargs[key]
        kwargs['new_email__iexact'] = value
        if EmailChange.objects.filter(**kwargs).count():
            raise ValidationError(self.msg, code=self.code)

validate_email_not_used = EmailNotUsedValidator()
