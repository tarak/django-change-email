from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from change_email.models import EmailChange


class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = EmailChange
        exclude = ('user',)

    def clean_new_email(self):
        """
        Validates that the given email address is not taken.
        """
        new_email = self.cleaned_data["new_email"]
        users = User.objects.filter(email__iexact=new_email).count()
        email_changes = EmailChange.objects.filter(new_email__iexact=new_email).count()
        if users > 0 or email_changes > 0:
            msg = _("This email address is taken.")
            raise forms.ValidationError(msg)
        return new_email
