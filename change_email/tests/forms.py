from django.contrib.auth.models import User
from django.test import TestCase

from change_email import forms
from change_email.models import EmailChange


class EmailChangeFormTestCase(TestCase):
    def test_change_email_form(self):
        """
        Test that ``EmailChangeForm`` enforces an email address that is
        not already taken by an existing user or a pending email address
        change request.

        """
        self.bob = User.objects.create_user('bob', 'bob@example.com', 'secret')
        self.alice = User.objects.create_user('alice', 'alice@example.com', 'secret')
        self.pending_request = EmailChange.objects.create(new_email='bob2@example.com', user=self.bob)
        invalid_data_dicts = [
            # Existing user.
            {'data': {'new_email': 'alice@example.com'},
            'error': ('new_email', [u"This email address is already in use. Please supply a different email address."])},
            # Existing email address change request.
            {'data': {'new_email': 'bob2@example.com'},
            'error': ('new_email', [u"This email address is already in use. Please supply a different email address."])},
            ]

        for invalid_dict in invalid_data_dicts:
            form = forms.EmailChangeForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])
        form = forms.EmailChangeForm(data={'new_email': 'alice2@example.com'})
        self.failUnless(form.is_valid())
        self.pending_request.delete()
        self.bob.delete()
        self.alice.delete()
