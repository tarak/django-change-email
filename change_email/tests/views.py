from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from change_email import app_settings
from change_email import forms
from change_email.models import EmailChange
from change_email.tokens import default_token_generator


EMAIL_CHANGE_DELETE_SUCCESS_REDIRECT_URL = getattr(app_settings, 'EMAIL_CHANGE_DELETE_SUCCESS_REDIRECT_URL')


class EmailChangeViewsTestCase(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user('alice', 'alice@example.com', 'secret')
        self.bob = User.objects.create_user('bob', 'bob@example.com', 'secret')
        self.client.login(username='bob', password='secret')

    def test_email_address_change_creation(self):
        """
        A ``GET`` to the ``change_email_create`` view uses the appropriate
        template and populates the email change form into the context.

        """
        response = self.client.get(reverse('change_email_create'))
        self.assertEqual(response.status_code, 200)
        self.failUnless(isinstance(response.context['form'],
                                   forms.EmailChangeForm))
        self.assertTemplateUsed(response,
                                'change_email/emailchange_form.html')

    def test_email_address_change_creation_success(self):
        """
        A ``POST`` to the ``change_email_create`` view with valid data properly
        creates a new email address change request and issues a redirect.

        """
        response = self.client.post(reverse('change_email_create'), data={'new_email': 'bob2@example.com',})
        self.assertEqual(EmailChange.objects.count(), 1)
        object = EmailChange.objects.get()
        self.assertEqual(len(mail.outbox), 1)
        self.assertRedirects(response,
                             'http://testserver%s' % reverse('change_email_detail', args=[object.id,]))
        object.delete()
        mail.outbox = []

    def test_email_address_change_creation_failure(self):
        """
        A ``POST`` to the ``change_email_create`` view with pnvalid data properly
        fails and issues the according error.

        """
        response = self.client.post(reverse('change_email_create'),
                                    data={'new_email': 'bob@example.com'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field='new_email',
                             errors=u"This email address is already in use. Please supply a different email address.")
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(reverse('change_email_create'),
                                    data={'new_email': 'alice@example.com'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field='new_email',
                             errors=u"This email address is already in use. Please supply a different email address.")
        self.assertEqual(len(mail.outbox), 0)

    def test_email_address_change_creation_already_existing(self):
        """
        A ``POST`` to the ``change_email_create`` view when a pending request
        already exists issues a redirect to the ``change_email_detail`` view
        of the existing request.

        """
        self.pending_request = EmailChange.objects.create(new_email='bob2@example.com', user=self.bob)
        response = self.client.post(reverse('change_email_create'),
                                    data={'new_email': 'bob2@example.com'})
        self.assertRedirects(response,
                             'http://testserver%s' % reverse('change_email_detail', args=[self.pending_request.id,]))
        self.pending_request.delete()

    def test_email_address_change_confirmation_success(self):
        """
        A ``GET`` to the ``change_email_confirm`` view with the valid token works.
        """
        self.pending_request = EmailChange.objects.create(new_email='bob2@example.com', user=self.bob)
        token = default_token_generator.make_token(self.bob)
        response = self.client.get(reverse('change_email_confirm', args=[token,]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['confirmed'])
        bob = User.objects.filter(username='bob').get()
        self.assertEqual(bob.email, 'bob2@example.com')
        self.assertEqual(EmailChange.objects.filter(new_email='bob2@example.com').count(), 0)

    def test_email_address_change_confirmation_failure(self):
        """
        A ``GET`` to the ``change_email_confirm`` view with an invalid token does not work.
        """
        self.pending_request = EmailChange.objects.create(new_email='bob2@example.com', user=self.bob)
        token = 'foo'
        response = self.client.get(reverse('change_email_confirm', args=[token,]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['confirmed'])
        self.assertEqual(EmailChange.objects.filter(new_email='bob2@example.com').count(), 1)
        self.pending_request.delete()

    def test_email_address_change_confirmation_non_existing(self):
        """
        A ``GET`` to the ``change_email_confirm`` view when no pending request
        exist issues a redirect to the ``change_email_create`` view.

        """
        token = 'foo'
        response = self.client.get(reverse('change_email_confirm', args=[token,]))
        self.assertRedirects(response,
                             'http://testserver%s' % reverse('change_email_create'))

    def test_email_address_change_deletion(self):
        """
        A ``GET`` to the ``change_email_delete`` view works.

        """
        self.pending_request = EmailChange.objects.create(new_email='bob2@example.com', user=self.bob)
        response = self.client.get(reverse('change_email_delete', args=[self.pending_request.id,]))
        self.assertEqual(response.status_code, 200)
        self.pending_request.delete()

    def test_email_address_change_deletion_non_existing(self):
        """
        A ``GET`` to the ``change_email_delete`` view when no pending request
        exist issues a redirect to the ``change_email_create`` view.

        """
        response = self.client.get(reverse('change_email_delete', args=[1,]))
        self.assertRedirects(response,
                             'http://testserver%s' % reverse('change_email_create'))

    def test_email_address_change_deletion_success(self):
        """
        A ``POST`` to the ``change_email_delete`` view with valid data works.

        """
        self.pending_request = EmailChange.objects.create(new_email='bob2@example.com', user=self.bob)
        response = self.client.post(reverse('change_email_delete', args=[self.pending_request.id,]))
        self.assertEqual(EmailChange.objects.filter(new_email='bob2@example.com').count(), 0)
        self.pending_request.delete()

    def test_email_address_change_detail(self):
        """
        A ``GET`` to the ``change_email_detail`` view with valid data works.

        """
        self.pending_request = EmailChange.objects.create(new_email='bob2@example.com', user=self.bob)
        response = self.client.get(reverse('change_email_detail', args=[self.pending_request.id,]))
        self.assertEqual(response.status_code, 200)
        self.pending_request.delete()

    def test_email_address_change_detail_non_existing(self):
        """
        A ``GET`` to the ``change_email_detail`` view when no pending request
        exist issues a redirect to the ``change_email_create`` view.


        """
        response = self.client.get(reverse('change_email_detail', args=[1000]))
        self.assertRedirects(response,
                             'http://testserver%s' % reverse('change_email_create'))
