from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^locked-out/', lambda: None, name='locked_out')
]