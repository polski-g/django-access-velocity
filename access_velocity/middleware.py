import datetime
import logging

from django.utils.deprecation import MiddlewareMixin
from django.urls import get_callable

from ipware.ip import get_real_ip

from access_velocity.conf import settings
from access_velocity import utils


logger = logging.getLogger(settings.ACCESS_VELOCITY_LOGGER)


def _get_failure_view():
    return get_callable(settings.ACCESS_VELOCITY_LOCKOUT_VIEW)


class AccessVelocityMiddleware(MiddlewareMixin):
    @staticmethod
    def _reject(request):
        reason = settings.ACCESS_VELOCITY_COOLOFF_MESSAGE
        logger.warning(
            'Forbidden (%s): %s', reason, request.path,
            extra={
                'status_code': 403,
                'request': request,
            }
        )
        return _get_failure_view()(request, reason=reason)

    def process_view(self, request, *args):
        # do nothing if user is not logged in
        if not hasattr(request, 'user') or request.user.is_anonymous():
            return None

        # do nothing if can't get real IP
        real_ip = get_real_ip(request)
        if real_ip is None:
            return None

        # reject if user is banned
        if utils.is_user_locked_out(request.user.id):
            return self._reject(request)

        try:
            previous_info = utils.get_last_known_ip(request.user.id)
            if previous_info:
                previous_ip = previous_info[0]
                if previous_ip != real_ip:
                    msg = "User ID %s current IP != previous IP (from %s to %s)" % \
                          (str(request.user.id), previous_ip, real_ip)
                    logger.info(msg)

                    _distance = utils.get_distance(previous_ip, real_ip)
                    then = datetime.datetime.fromtimestamp(previous_info[1])
                    if not _distance:
                        return None

                    _velocity = utils.get_velocity(_distance, then)
                    if _velocity > settings.ACCESS_VELOCITY_MAX_VELOCITY:
                        logger.warning('User ID {0} has a estimated velocity of {1:.2f}ft/sec. Blocking access.'.format(
                            request.user.id, _velocity))
                        utils.lock_out_user(request.user.id)
                        return self._reject(request)
        finally:
            utils.set_known_ip(request.user.id, real_ip)

        return None
