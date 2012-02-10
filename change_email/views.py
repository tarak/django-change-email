import logging

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from change_email import app_settings
from change_email.forms import EmailChangeForm
from change_email.models import EmailChange
from change_email.mail import send_confirmation


logger = logging.getLogger(__name__)


class EmailChangeConfirmView(TemplateView):
    """
    A class based generic view (TemplateView) to confirm an
    email address change request.

    This view is protected by the ``login-required`` decorator.

    If a :model:`change_email.EmailChange` object that
    has been created by the user is not found, the user will be
    redirected to :view:`change_email.views.EmailChangeCreateView`.

    **Context:**

    ``object``
        An instance of :model:`change_email.EmailChange`.

    **Template:**

    :template:`change_email/emailchange_confirm.html`

    Class based generic views are further documented in
    the Django documentation.

    """
    template_name = "change_email/emailchange_confirm.html"
    object = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            object = EmailChange.objects.filter(user=request.user).get()
        except EmailChange.DoesNotExist:
            msg = _("No email address change request was found. Either an old one has expired or a new one has not been requested.")
            messages.add_message(request, messages.ERROR, msg)
            logger.error('No email address change request found.')
            return HttpResponseRedirect(reverse('change_email_create'))
        self.object = object
        return super(EmailChangeConfirmView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EmailChangeConfirmView, self).get_context_data(**kwargs)
        context['confirmed'] = False
        if default_token_generator.check_token(self.request.user, self.kwargs['token']):
            context['confirmed'] = True
            self.request.user.email = self.object.new_email
            self.request.user.save()
            self.object.delete()
        return context


class EmailChangeCreateView(CreateView):
    """
    A class based generic view (CreateView) to create
    a :model:`change_email.EmailChange` object.

    This view is protected by the ``login-required`` decorator.

    If a :model:`change_email.EmailChange` object that
    has been created by the user is found, the user will be
    redirected to :view:`change_email.views.EmailChangeDetailView`.

    Class based generic views are further documented in
    the Django documentation.
    """
    model = EmailChange
    form_class = EmailChangeForm
    template_name_txt = 'change_email/emailchange_email.txt'
    template_name_html = 'change_email/emailchange_email.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if EmailChange.objects.filter(user=request.user).count():
            msg = _("An email address change request was found. It must be deleted before a new one can be requested.")
            messages.add_message(request, messages.ERROR, msg)
            logger.error('Pending email address change request found.')
            return HttpResponseRedirect(reverse('change_email_index'))
        return super(EmailChangeCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        send_confirmation(object,
                  template_name_txt=self.template_name_txt,
                  template_name_html=self.template_name_html)
        msg = _("The email address change request was processed.")
        messages.add_message(self.request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('change_email_index'))


class EmailChangeDeleteView(DeleteView):
    """
    A class based generic view (DeleteView) to delete a
    :model:`change_email.EmailChange` object.

    This view is protected by the ``login-required`` decorator.

    If a :model:`change_email.EmailChange` object that
    has been created by the user is not found, the user will be
    redirected to :view:`change_email.views.EmailChangeCreateView`.

    Class based generic views are further documented in
    the Django documentation.
    """
    model = EmailChange

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not EmailChange.objects.filter(user=request.user).count():
            msg = _("No email address change request was found. Either an old one has expired or a new one has not been requested.")
            messages.add_message(request, messages.ERROR, msg)
            logger.error('No email address change request found.')
            return HttpResponseRedirect(reverse('change_email_create'))
        return super(EmailChangeDeleteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self,  **kwargs):
        return reverse('change_email')


class EmailChangeDetailView(DetailView):
    """
    A class based generic detail view (DetailView) to display a
    :model:`change_email.EmailChange` object.

    This view is protected by the ``login-required`` decorator.

    If a :model:`change_email.EmailChange` object that
    has been created by the user is not found, the user will be
    redirected to :view:`change_email.views.EmailChangeCreateView`.

    Class based generic views are further documented in
    the Django documentation.
    """
    model = EmailChange

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not EmailChange.objects.filter(user=request.user).count():
            msg = _("No email address change request was found. Either an old one has expired or a new one has not been requested.")
            messages.add_message(request, messages.ERROR, msg)
            logger.error('No email address change request found.')
            return HttpResponseRedirect(reverse('change_email_create'))
        return super(EmailChangeDetailView, self).dispatch(request, *args, **kwargs)


class EmailChangeIndexView(RedirectView):
    """
    A class based generic view (RedirectView) to redirect
    users to other views.

    This view is protected by the ``login-required`` decorator.

    If a :model:`change_email.EmailChange` object is found that
    has been created by the user, the user will be redirected to
    :view:`change_email.views.EmailChangeDetailView`. If such an
    object is not found the user will be redirected
    to :view:`change_email.views.EmailChangeCreateView`.

    Class based generic views are further documented in
    the Django documentation.
    """
    permanent = False

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EmailChangeIndexView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self,  **kwargs):
        try:
            object = EmailChange.objects.filter(user=self.request.user).get()
            return reverse('change_email_detail', args=[object.pk])
        except EmailChange.DoesNotExist:
            return reverse('change_email_create')
