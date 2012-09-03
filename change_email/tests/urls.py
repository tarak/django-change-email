from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^account/', include('change_email.urls')),
)
