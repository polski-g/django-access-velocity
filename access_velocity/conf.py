from __future__ import unicode_literals

from django.conf import settings

from appconf import AppConf


class MyAppConf(AppConf):
    LOGGER = 'access_velocity'

    # maximum allowable velocity in ft/sec
    MAX_VELOCITY = 200

    # time IPs stay in cache and used in calculating velocity
    TIME_DELTA = 240

    # time an authenticated user is locked out for violating MAX_VELOCITY
    LOCKOUT_TIME = 21600

    # Returns the view to be used for restrictions
    LOCKOUT_VIEW = 'access_velocity.views.locked_out'

    COOLOFF_MESSAGE = 'Access restricted due to suspicious activity. Contact administrator if you think this was in error.'

    class Meta:
        prefix = 'access_velocity'
