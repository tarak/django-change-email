from django.conf.urls.defaults import *

from change_email.views import EmailChangeConfirmView
from change_email.views import EmailChangeCreateView
from change_email.views import EmailChangeDeleteView
from change_email.views import EmailChangeDetailView
from change_email.views import EmailChangeIndexView

urlpatterns = patterns('',
                       url(r'^email/change/$', EmailChangeIndexView.as_view(), name='change_email_index'),
                       url(r'^email/change/confirm/(?P<token>.+)/$', EmailChangeConfirmView.as_view(), name='change_email_confirm'),
                       url(r'^email/change/create/$', EmailChangeCreateView.as_view(), name='change_email_create'),
                       url(r'^email/change/delete/(?P<pk>\d+)/$', EmailChangeDeleteView.as_view(), name='change_email_delete'),
                       url(r'^email/change/(?P<pk>\d+)/$', EmailChangeDetailView.as_view(), name='change_email_detail'),
                       )
