from __future__ import unicode_literals

from django.http import HttpResponseForbidden


def locked_out(request, reason):
    return HttpResponseForbidden('You have been locked out because: %s' % reason, content_type='text/plain')
