from django import forms
from django.utils.translation import ugettext_lazy as _

from change_email.models import EmailChange
from change_email.validators import validate_email_not_used


class EmailChangeForm(forms.ModelForm):
    """
A form to allow users to change the email address they have
registered with.

Just consists of an ``forms.EmailField`` with a
:validator:`validate_email_not_used` validator to check if a
given email address is not already used.
"""
    new_email = forms.EmailField(help_text=_('Please enter your'
                                             ' new email address.'),
                                 label=_('new email address'),
                                 validators=[validate_email_not_used])

    class Meta:
        model = EmailChange
        exclude = ('user', 'site')
