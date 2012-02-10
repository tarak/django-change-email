===================
Django-Change-Email
===================
:Info: A Django application to enable users to change their e-mail  address.
:Author: Tarak Blah (http://github.com/tarak)

Overview
=================
django-change-email enables registered users to change their e-mail address.

The user can request a change of e-mail address. An e-mail is sent to the new
address containing a confirmation URL that must be visited for the new address
to be validated.

Users can see pending change requests and delete them if necessary.

Requirements
=================
This application requires the built-in Django messages application.

Installation
=================
Currently only manual installation is available.

Check out the repository using git:

    git clone http://github.com/tarak/django-change-email

Install using the setup.py script:

    python setup.py install

Add ``change_email`` to the ``INSTALLED_APPS`` setting of your project and run

    python manage.py syncdb

in your project's root directory.

Configuration
=================
The following settings can be defined:


:EMAIL_CHANGE_VERIFICATION_DAYS: An integer determining the number of days users
    will have to confirm their email change request. If a user does not confirm
    the request within that period, the request may be deleted by maintenance
    scripts provided with django-change-email. Defaults to 2 days.
:EMAIL_CHANGE_FROM_EMAIL: E-mail address to use as ``from`` address in the
    confirmation mail. Defaults to settings.DEFAULT_FROM_EMAIL.
:EMAIL_CHANGE_HTML_EMAIL: A boolean determining if a multi-part email is to be
    sent to confirm the request. This makes it possible to send HTML-emails.
    Defaults to False.

Maintenance
=================
Django-Change-Email includes a management command to delete expired change
requests:

    python manage.py cleanupemailchangerequests

This command will delete all requests older than
``EMAIL_CHANGE_VERIFICATION_DAYS``.

Setting up URL's
=================
The application includes a Django ``URLconf`` which sets up URL patterns for
the views in ``change_email.views``.

This ``URLconf`` can be found in ``change_email.urls`` and can be included
in your project's root URL configuration. For example, to place the
URLs under the prefix ``/account/``, you could add the following to
your project's root ``URLconf``:

    (r'^account/', include('change_email.urls'))

Users would then be able to visit the URL ``/account/email/change/`` where they
will be redirected to other views.

Views
================
All views are class based generic views. Documentation of these views are
included in the Django documentation.

All views are documented conforming to the Django admin documentation generator.


:EmailChangeConfirmView: This view expects a confirmation token as an argument.
    If the token is valid it changes the e-mail address of the user in the
    User-model and deletes the change request.
:EmailChangeCreateView: Used to create a change request and to send the
    confirmation e-mail.
:EmailChangeDeleteView: Used to delete a pending change request.
:EmailChangeDetailView: Used to display a pending change request.
:EmailChangeIndexView: A redirecting view. If no change request
    exists the user will be redirected to ``EmailChangeCreateView``, otherwise
    to ``EmailChangeDetailView``.


Templates
===============
The templates for the views need to be named following the convention on naming
templates in Django class based generic views:


:change_mail/emailchange_confirm.html: Used in the view 
    ``EmailChangeConfirmView``.
:change_mail/emailchange_form.html: Used in the view
    ``EmailChangeCreateView``.
:change_mail/emailchange_confirm_delete.html: Used in the view
    ``EmailChangeDeleteView``.
:change_mail/emailchange_confirm.html: Used in the view 
    ``EmailChangeConfirmView``.


In order to send the confirmation email three templates must be created:

:change_mail/emailchange_subject.txt: Used as the email's subject.
:change_mail/emailchange_email.txt: Used as the message body of the text
    confirmation email.
:change_mail/emailchange_email.html: Used as the message body of the HTML
    confirmation email.
