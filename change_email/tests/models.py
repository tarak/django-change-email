import time
import datetime

from django.contrib.auth.models import User
from django.core import management

from change_email.conf import settings
from change_email.models import EmailChange
from change_email.tests.lib import BaseTest


class EmailChangeModelTestCase(BaseTest):

    fixtures = ['django_change_email_test_models_fixtures.json']

    def setUp(self):
        output = super(EmailChangeModelTestCase, self).setUp()
        self.alice = User.objects.get(username='alice')
        self.bob = User.objects.get(username='bob')
        self.timeout_days = settings.EMAIL_CHANGE_TIMEOUT
        return output

    def test_email_address_change_creation(self):
        """
        Creating a new email address change request populates the correct data.

        """
        request = EmailChange.objects.create(new_email='bob2@example.com',
                                             user=self.bob)
        self.assertEqual(request.user.id, self.bob.id)
        self.assertEqual(request.new_email, 'bob2@example.com')
        self.failIf(request.has_expired())
        request.delete()

    def test_email_address_change_has_expired(self):
        """
        Testing the model's token methods.

        """
        request1 = EmailChange.objects.create(new_email='bob2@example.com',
                                              user=self.bob)
        time.sleep(2)
        self.failUnless(request1.has_expired(seconds=1))
        self.failIf(request1.has_expired(seconds=1000))


    def test_email_address_change_management_command(self):
        """
        Testing the management command.

        """
        request1 = EmailChange.objects.create(new_email='bob2@example.com',
                                              user=self.bob)
        self.assertEqual(request1.user.id, self.bob.id)
        self.assertEqual(request1.new_email, 'bob2@example.com')
        self.failIf(request1.has_expired())
        request2 = EmailChange.objects.create(new_email='alice2@example.com',
                                              user=self.alice)
        self.assertEqual(request2.user.id, self.alice.id)
        self.assertEqual(request2.new_email, 'alice2@example.com')
        self.failIf(request2.has_expired())
        request2.date -= datetime.timedelta(days=self.timeout_days + 1)
        request2.save()
        new = 'alice2@example.com'
        request2 = EmailChange.objects.filter(new_email=new).get()
        self.failUnless(request2.has_expired())
        management.call_command('cleanupemailchangerequests')
        self.assertEqual(EmailChange.objects.count(), 1)
        self.assertEqual(EmailChange.objects.filter(new_email=new).count(), 0)
        new = 'bob2@example.com'
        self.assertEqual(EmailChange.objects.filter(new_email=new).count(), 1)
        request1.delete()
        request2.delete()

    def test_email_address_change_managers(self):
        """
        Testing the model managers.

        """
        request1 = EmailChange.objects.create(new_email='bob2@example.com',
                                              user=self.bob)
        self.assertEqual(request1.user.id, self.bob.id)
        self.assertEqual(request1.new_email, 'bob2@example.com')
        self.failIf(request1.has_expired())
        request2 = EmailChange.objects.create(new_email='alice2@example.com',
                                              user=self.alice)
        self.assertEqual(request2.user.id, self.alice.id)
        self.assertEqual(request2.new_email, 'alice2@example.com')
        self.failIf(request2.has_expired())
        request2.date -= datetime.timedelta(days=self.timeout_days + 1)
        request2.save()
        new_email = 'alice2@example.com'
        request2 = EmailChange.objects.filter(new_email=new_email).get()
        self.failUnless(request2.has_expired())
        self.assertEqual(EmailChange.expired_objects.count(), 1)
        self.assertEqual(EmailChange.pending_objects.count(), 1)
        request1.delete()
        request2.delete()
