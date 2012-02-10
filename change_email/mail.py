from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _

from change_email import app_settings
from change_email.tokens import default_token_generator


EMAIL_CHANGE_FROM_EMAIL = getattr(app_settings, 'EMAIL_CHANGE_FROM_EMAIL')
EMAIL_CHANGE_HTML_EMAIL = getattr(app_settings, 'EMAIL_CHANGE_HTML_EMAIL')


def send_confirmation(object, template_name_subject="change_email/emailchange_subject.txt",
              template_name_txt="change_email/emailchange_email.txt",
              template_name_html="change_email/emailchange_email.html"):
    current_site = Site.objects.get_current()
    token = default_token_generator.make_token(object.user)
    c = {
        'object': object,
        'token':  token,
        'current_site':  current_site,
    }
    t = loader.get_template(template_name_subject)
    subject_content = t.render(Context(c))
    subject_content = subject_content.rstrip('\n')
    t = loader.get_template(template_name_txt)
    text_content = t.render(Context(c))
    if EMAIL_CHANGE_HTML_EMAIL:
        t = loader.get_template(template_name_html)
        html_content = t.render(Context(c))
        msg = EmailMultiAlternatives(subject_content, text_content, EMAIL_CHANGE_FROM_EMAIL, [object.new_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    else:
        send_mail(subject_content, text_content, EMAIL_CHANGE_FROM_EMAIL, [object.new_email])
