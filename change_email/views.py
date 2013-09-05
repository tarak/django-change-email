import logging

from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from change_email.conf import settings
from change_email.forms import EmailChangeForm
from change_email.models import EmailChange
from change_email.signals import email_change_confirmed
from change_email.signals import email_change_created
from change_email.signals import email_change_deleted


logger = logging.getLogger(__name__)


class EmailChangeConfirmView(TemplateView):
    """
A view to confirm an email address change request.
"""
    template_name = "change_email/emailchange_confirm.html"
    """The template used to render this view."""

    object = None
    """An instance of :model:`EmailChange`, if found."""

    def __init__(self, *args, **kwargs):
        super(EmailChangeConfirmView, self).__init__(*args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
If an :model:`EmailChange` object that
has been created by the user is not found, the user will be
redirected to :view:`EmailChangeCreateView`.
"""
        try:
            object = EmailChange.objects.filter(user=request.user).get()
        except EmailChange.DoesNotExist:
            msg = _("No email address change request was found. Either an old "
                    "one has expired or a new one has not been requested.")
            messages.add_message(request,
                                 messages.ERROR,
                                 msg,
                                 fail_silently=True)
            logger.error('No email address change request found.')
            #return HttpResponseRedirect(reverse_lazy('change_email_create'))
            object = None
        self.object = object
        return super(EmailChangeConfirmView, self).dispatch(request,
                                                            *args,
                                                            **kwargs)

    def get_context_data(self, **kwargs):
        """
Inserts following variables into the context:

``object``
    An instance of :model:`EmailChange`.

``confirmed``
    A boolean determining if the change request has been confirmed
    succesfully.
"""
        kwargs['object'] = self.object
        kwargs['confirmed'] = False
        if self.object and self.object.check_signature(self.kwargs['signature']):
            kwargs['confirmed'] = True
            self.save()
        if kwargs['confirmed']:
            msg = _("The email address change was confirmed. Your new email"
                    " address will be used as primary address.")
            messages.add_message(self.request,
                                 messages.INFO,
                                 msg,
                                 fail_silently=True)
        else:
            msg = _("The email address change has not been confirmed."
                    " Please request a new one.")
            messages.add_message(self.request,
                                 messages.ERROR,
                                 msg,
                                 fail_silently=True)
            logger.error('Email address change request was not confirmed.')
        return super(EmailChangeConfirmView, self).get_context_data(**kwargs)

    def save(self):
        """
Saves the new email address to :class:`django.contrib.auth.models.User` and
send a :signal:`email_change_confirmed` signal.
"""
        setattr(self.request.user, settings.EMAIL_CHANGE_FIELD,
                self.object.new_email)
        #self.request.user.email = self.object.new_email
        self.request.user.save()
        self.object.delete()
        email_change_confirmed.send(sender=self, request=self.request)


class EmailChangeCreateView(CreateView):
    """
A view to create an :model:`EmailChange` object.
"""
    model = EmailChange

    form_class = EmailChangeForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
If an :model:`EmailChange` object that
has been created by the user is found, the user will be
redirected to :view:`EmailChangeDetailView`.
"""
        if EmailChange.objects.filter(user=request.user).count():
            msg = _("An email address change request was found. It must"
                    " be deleted before a new one can be requested.")
            messages.add_message(request,
                                 messages.ERROR,
                                 msg,
                                 fail_silently=True)
            logger.error('Pending email address change request found.')
            object = EmailChange.objects.filter(user=request.user).get()
            return HttpResponseRedirect(reverse_lazy('change_email_detail',
                                                     args=[object.pk]))
        return super(EmailChangeCreateView, self).dispatch(request,
                                                           *args,
                                                           **kwargs)

    def form_valid(self, form):
        """
Saves the email address change request, sends an email to confirm the
request, adds a success message for the user and redirects to
:view:`EmailChangeDetailView`.
"""
        form.instance.user = self.request.user
        instance = super(EmailChangeCreateView, self).form_valid(form)
        msg = _("The email address change request was processed.")
        messages.add_message(self.request,
                             messages.INFO,
                             msg,
                             fail_silently=True)
        email_change_created.send(sender=self, request=self.request)
        form.instance.send_confirmation_mail(self.request)
        return instance
    form_valid = transaction.commit_on_success(form_valid)


class EmailChangeDeleteView(DeleteView):
    """
A view to delete an :model:`EmailChange` object.
"""
    model = EmailChange

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
If an :model:`EmailChange` object that
has been created by the user is not found, the user will be
redirected to :view:`EmailChangeCreateView`.
"""
        if not EmailChange.objects.filter(user=request.user).count():
            msg = _("No email address change request was found. Either an "
                    "old one has expired or a new one has not been requested.")
            messages.add_message(request,
                                 messages.ERROR,
                                 msg,
                                 fail_silently=True)
            logger.error('No email address change request found.')
            return HttpResponseRedirect(reverse_lazy('change_email_create'))
        return super(EmailChangeDeleteView, self).dispatch(request,
                                                           *args,
                                                           **kwargs)

    def get_success_url(self, **kwargs):
        """
Returns the URL to redirect to after an email address change request has
been deleted by an user. The URL to redirect to can be customized by setting
:py:attr:`~password_policies.conf.Settings.EMAIL_CHANGE_DELETE_SUCCESS_REDIRECT_URL`.
"""
        msg = _("The email address change request was deleted.")
        messages.add_message(self.request,
                             messages.INFO,
                             msg,
                             fail_silently=True)
        email_change_deleted.send(sender=self, request=self.request)
        return reverse_lazy('change_email_create')


class EmailChangeDetailView(DetailView):
    """
A view to display an :model:`EmailChange` object.
"""
    model = EmailChange

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
If an :model:`EmailChange` object that has been created by the user is not
found, the user will be redirected to :view:`EmailChangeCreateView`.
"""
        if not EmailChange.objects.filter(user=request.user).count():
            msg = _("No email address change request was found. Either an "
                    "old one has expired or a new one has not been requested.")
            messages.add_message(request,
                                 messages.ERROR,
                                 msg,
                                 fail_silently=True)
            logger.error('No email address change request found.')
            return HttpResponseRedirect(reverse_lazy('change_email_create'))
        return super(EmailChangeDetailView, self).dispatch(request,
                                                           *args,
                                                           **kwargs)


class EmailChangeIndexView(RedirectView):
    """
A view to redirect users to other views.
"""
    permanent = False
    """
Determines that this view will always issue a HTTP 307 (Temporary
Redirect) status code.
"""

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EmailChangeIndexView, self).dispatch(request,
                                                          *args,
                                                          **kwargs)

    def get_redirect_url(self, **kwargs):
        """
If an :model:`EmailChange` object is found that
has been created by the user, the user will be redirected to
:view:`EmailChangeDetailView`. If such an
object is not found the user will be redirected
to :view:`EmailChangeCreateView`.
"""
        user = self.request.user
        try:
            object = EmailChange.objects.filter(user=user).get()
            return reverse_lazy('change_email_detail', args=[object.pk])
        except EmailChange.DoesNotExist:
            return reverse_lazy('change_email_create')
