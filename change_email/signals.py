from django.dispatch import Signal


# A user has completed a change of email address.
email_change_confirmed = Signal(providing_args=["request"])

# A user has requested a change of email address.
email_change_created = Signal(providing_args=["request"])

# A user has deleted a change of email address.
email_change_deleted = Signal(providing_args=["request"])
