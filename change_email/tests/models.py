import datetime

from django.contrib.auth.models import User
from django.core import management
from django.test import TestCase

from change_email import app_settings
from change_email.models import EmailChange


EMAIL_CHANGE_EXPIRATION_DAYS = getattr(app_settings, 'EMAIL_CHANGE_EXPIRATION_DAYS')

class EmailChangeModelTestCase(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user('alice', 'alice@example.com', 'secret')
        self.bob = User.objects.create_user('bob', 'bob@example.com', 'secret')

    def test_email_address_change_creation(self):
        """
        Creating an new email address change request populates the correct data.

        """
        self.pending_request = EmailChange.objects.create(new_email='bob2@example.com', user=self.bob)
        self.assertEqual(self.pending_request.user.id, self.bob.id)
        self.assertEqual(self.pending_request.new_email, 'bob2@example.com')
        self.failIf(self.pending_request.has_expired())
        self.pending_request.delete()

    def test_email_address_change_management_command(self):
        """
        Testing the management command.

        """
        self.pending_request1 = EmailChange.objects.create(new_email='bob2@example.com', user=self.bob)
        self.assertEqual(self.pending_request1.user.id, self.bob.id)
        self.assertEqual(self.pending_request1.new_email, 'bob2@example.com')
        self.failIf(self.pending_request1.has_expired())
        self.pending_request2 = EmailChange.objects.create(new_email='alice2@example.com', user=self.alice)
        self.assertEqual(self.pending_request2.user.id, self.alice.id)
        self.assertEqual(self.pending_request2.new_email, 'alice2@example.com')
        self.failIf(self.pending_request2.has_expired())
        self.pending_request2.date -= datetime.timedelta(days=EMAIL_CHANGE_EXPIRATION_DAYS + 1)
        self.pending_request2.save()
        self.pending_request2 = EmailChange.objects.filter(new_email='alice2@example.com').get()
        self.failUnless(self.pending_request2.has_expired())
        management.call_command('cleanupemailchangerequests')
        self.assertEqual(EmailChange.objects.count(), 1)
        self.assertEqual(EmailChange.objects.filter(new_email='alice2@example.com').count(), 0)
        self.assertEqual(EmailChange.objects.filter(new_email='bob2@example.com').count(), 1)
        self.pending_request1.delete()
        self.pending_request2.delete()
