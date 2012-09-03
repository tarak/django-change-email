from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from change_email.models import EmailChange


class EmailNotUsedValidator(object):
    """
A validator to check if a given email address is already taken.
"""
    code = "email_in_use"
    msg = _("This email address is already in use."
            " Please supply a different email address.")

    def __call__(self, value):
        if User.objects.filter(email__iexact=value).count():
            raise ValidationError(self.msg, code=self.code)
            return
        if EmailChange.objects.filter(new_email__iexact=value).count():
            raise ValidationError(self.msg, code=self.code)
        return

validate_email_not_used = EmailNotUsedValidator()
