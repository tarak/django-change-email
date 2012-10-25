import os

from django.contrib.auth.models import User
from django.test import TestCase

from change_email import forms
from change_email.models import EmailChange
from change_email.tests.lib import BaseTest


class EmailChangeFormTestCase(BaseTest):

    fixtures = ['django_change_email_test_forms_fixtures.json']

    def test_change_email_form(self):
        """
        Test that ``EmailChangeForm`` enforces an email address that is
        not already taken by an existing user or a pending email address
        change request.

        """
        msg = u"This email address is already in use."
        msg = msg + u" Please supply a different email address."
        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        pending_request = EmailChange.objects.get(user=bob)
        invalid_data_dicts = [
            # Invalid email.
            {'data': {'new_email': 'alice'},
            'error': ('new_email', [u"Enter a valid email address."])},
            # Existing user.
            {'data': {'new_email': 'alice@example.com'},
            'error': ('new_email', [msg])},
            # Existing email address change request.
            {'data': {'new_email': 'bob2@example.com'},
            'error': ('new_email', [msg])},
            ]

        for invalid_dict in invalid_data_dicts:
            form = forms.EmailChangeForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])
        form = forms.EmailChangeForm(data={'new_email': 'alice2@example.com'})
        self.failUnless(form.is_valid())
