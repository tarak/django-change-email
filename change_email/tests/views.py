from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse

from change_email.forms import EmailChangeForm
from change_email.models import EmailChange
from change_email.tests.lib import BaseTest


class EmailChangeViewsTestCase(BaseTest):

    fixtures = ['django_change_email_test_views_fixtures.json']

    def setUp(self):
        output = super(EmailChangeViewsTestCase, self).setUp()
        self.alice = User.objects.get(username='alice')
        self.bob = User.objects.get(username='bob')
        self.client.login(username='bob', password='Oor0ohf4bi-')
        return output

    def test_email_address_change_creation(self):
        """
        A ``GET`` to the ``change_email_create`` view uses the appropriate
        template and populates the email change form into the context.

        """
        response = self.client.get(reverse('change_email_create'))
        self.assertEqual(response.status_code, 200)
        self.failUnless(isinstance(response.context['form'],
                                   EmailChangeForm))
        self.assertTemplateUsed(response,
                                'change_email/emailchange_form.html')

    def test_email_address_change_creation_success(self):
        """
        A ``POST`` to the ``change_email_create`` view with valid data properly
        creates a new email address change request and issues a redirect.

        """
        response = self.client.post(reverse('change_email_create'),
                                    data={'new_email': 'bob2@example.com'})
        self.assertEqual(EmailChange.objects.count(), 1)
        object = EmailChange.objects.get()
        self.assertEqual(len(mail.outbox), 1)
        self.assertRedirects(response,
                             'http://testserver%s' % reverse('change_email_detail',
                                                             args=[object.id]))
        object.delete()
        mail.outbox = []

    def test_email_address_change_creation_failure(self):
        """
        A ``POST`` to the ``change_email_create`` view with invalid data properly
        fails and issues the according error.

        """
        msg = u"This email address is already in use."
        msg = msg + u" Please supply a different email address."
        response = self.client.post(reverse('change_email_create'),
                                    data={'new_email': 'bob@example.com'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field='new_email',
                             errors=msg)
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(reverse('change_email_create'),
                                    data={'new_email': 'alice@example.com'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field='new_email',
                             errors=msg)
        self.assertEqual(len(mail.outbox), 0)

    def test_email_address_change_creation_already_existing(self):
        """
        A ``POST`` to the ``change_email_create`` view when a pending request
        already exists issues a redirect to the ``change_email_detail`` view
        of the existing request.

        """
        request = EmailChange.objects.create(new_email='bob2@example.com',
                                                          user=self.bob)
        response = self.client.post(reverse('change_email_create'),
                                    data={'new_email': 'bob2@example.com'})
        self.assertRedirects(response,
                             'http://testserver%s' % reverse('change_email_detail',
                                                             args=[request.id]))
        request.delete()

    def test_email_address_change_confirmation_success(self):
        """
        A ``GET`` to the ``change_email_confirm`` view with the valid signature works.
        """
        request = EmailChange.objects.create(new_email='bob2@example.com',
                                                          user=self.bob)
        signature = request.make_signature()
        response = self.client.get(reverse('change_email_confirm', args=[signature,]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['confirmed'])
        bob = User.objects.filter(username='bob').get()
        self.assertEqual(bob.email, 'bob2@example.com')
        self.assertEqual(EmailChange.objects.filter(new_email='bob2@example.com').count(), 0)

    def test_email_address_change_confirmation_failure(self):
        """
        A ``GET`` to the ``change_email_confirm`` view with an invalid signature does not work.
        """
        request = EmailChange.objects.create(new_email='bob2@example.com',
                                                          user=self.bob)
        signature = 'foo'
        response = self.client.get(reverse('change_email_confirm', args=[signature,]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['confirmed'])
        self.assertEqual(EmailChange.objects.filter(new_email='bob2@example.com').count(), 1)
        request.delete()

    def test_email_address_change_confirmation_non_existing(self):
        """
        A ``GET`` to the ``change_email_confirm`` view when no pending request
        exist issues a redirect to the ``change_email_create`` view.

        """
        signature = 'foo'
        response = self.client.get(reverse('change_email_confirm', args=[signature,]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['confirmed'])

    def test_email_address_change_deletion(self):
        """
        A ``GET`` to the ``change_email_delete`` view works.

        """
        request = EmailChange.objects.create(new_email='bob2@example.com',
                                                          user=self.bob)
        response = self.client.get(reverse('change_email_delete',
                                           args=[request.id,]))
        self.assertEqual(response.status_code, 200)
        request.delete()

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
        request = EmailChange.objects.create(new_email='bob2@example.com', user=self.bob)
        response = self.client.post(reverse('change_email_delete',
                                            args=[request.id,]))
        self.assertEqual(EmailChange.objects.filter(new_email='bob2@example.com').count(), 0)
        request.delete()

    def test_email_address_change_detail(self):
        """
        A ``GET`` to the ``change_email_detail`` view with valid data works.

        """
        request = EmailChange.objects.create(new_email='bob2@example.com', user=self.bob)
        response = self.client.get(reverse('change_email_detail', args=[request.id,]))
        self.assertEqual(response.status_code, 200)
        request.delete()

    def test_email_address_change_detail_non_existing(self):
        """
        A ``GET`` to the ``change_email_detail`` view when no pending request
        exist issues a redirect to the ``change_email_create`` view.


        """
        response = self.client.get(reverse('change_email_detail', args=[1000]))
        self.assertRedirects(response,
                             'http://testserver%s' % reverse('change_email_create'))
