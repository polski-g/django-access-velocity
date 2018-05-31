import datetime
import time
import socket

from django.core.cache import cache
from django.contrib.gis.geoip2 import GeoIP2

import geoip2.errors
from geopy.distance import vincenty

from access_velocity.conf import settings


_geoip = GeoIP2()


def lat_lon(ip):
    try:
        return _geoip.lat_lon(ip)
    except geoip2.errors.AddressNotFoundError:
        return None
    except socket.gaierror:
        return None


def get_distance(ip1, ip2):
    """
    :param ip1: IP of former location (str)
    :param ip2: IP of new location (str)
    :return: distance in feet (float)
    """
    hop1_location = lat_lon(ip1)
    hop2_location = lat_lon(ip2)
    if hop1_location is None or hop2_location is None:
        return None
    _distance = vincenty(hop1_location, hop2_location).feet
    return _distance


def get_velocity(distance, time1, time2=None):
    """
    :param distance: in feet (can NOT be None)
    :param time1:
    :param time2: if None, assumed to be utcnow()
    :return: velocity in feet/second
    """
    if time2 is None:
        time2 = datetime.datetime.utcnow()
    elapsed = time2 - time1
    assert isinstance(elapsed, datetime.timedelta)
    _velocity = distance / elapsed.total_seconds()
    return _velocity


def is_user_locked_out(user_id):
    locked_key = 'access_velocity-locked-%s' % str(user_id)
    return cache.get(locked_key)


def lock_out_user(user_id):
    locked_key = 'access_velocity-locked-%s' % str(user_id)
    cache.set(locked_key, True, settings.ACCESS_VELOCITY_LOCKOUT_TIME)


def get_last_known_ip(user_id):
    """
    :param user_id:
    :return: tuple containing ip and seconds since epoch when this was stored
    """
    key = 'access_velocity-ip-%s' % str(user_id)
    return cache.get(key)


def set_known_ip(user_id, ip):
    now = datetime.datetime.utcnow()
    since_epoch = time.mktime(now.timetuple())
    key = 'access_velocity-ip-%s' % str(user_id)
    cache.set(key, (ip, since_epoch), settings.ACCESS_VELOCITY_TIME_DELTA)
