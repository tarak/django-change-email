from datetime import date

from django.conf import settings
from django.utils.http import int_to_base36, base36_to_int

from change_email import app_settings


EMAIL_CHANGE_VERIFICATION_DAYS = getattr(app_settings, 'EMAIL_CHANGE_VERIFICATION_DAYS')


class EmailChangeTokenGenerator(object):
    """
    Strategy object used to generate and check tokens for the email
    change mechanism.
    """
    def make_token(self, user):
        """
        Returns a token that can be used once to do a email change request
        for the given user.
        """
        num_days = self._num_days(self._today())
        return self._make_token_with_timestamp(user, num_days)

    def check_token(self, user, token):
        """
        Check that a email change request token is correct for a given user.
        """
        # Parse the token
        try:
            ts_b36, hash = token.split("-")
        except ValueError:
            return False
        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False
        # Check that the timestamp/uid has not been tampered with
        if self._make_token_with_timestamp(user, ts) != token:
            return False
        # Check the timestamp is within limit
        num_days = (self._num_days(self._today()) - ts)
        if num_days > EMAIL_CHANGE_VERIFICATION_DAYS:
            return False
        return True

    def _make_token_with_timestamp(self, user, timestamp):
        # timestamp is number of days since 2001-1-1.  Converted to
        # base 36, this gives us a 3 digit string until about 2121
        ts_b36 = int_to_base36(timestamp)
        # By hashing on the internal state of the user and using state
        # that is sure to change (the email salt will change as soon as
        # the new email address is set, at least for current Django auth),
        # we produce a hash that will be invalid as soon as it is used.
        # We limit the hash to 20 chars to keep URL short
        from django.utils.hashcompat import sha_constructor
        hash = sha_constructor(settings.SECRET_KEY + unicode(user.id) + user.password + user.email + unicode(timestamp)).hexdigest()[::2]
        return "%s-%s" % (ts_b36, hash)

    def _num_days(self, dt):
        return (dt - date(2001, 1, 1)).days

    def _today(self):
        # Used for mocking in tests
        return date.today()

default_token_generator = EmailChangeTokenGenerator()
