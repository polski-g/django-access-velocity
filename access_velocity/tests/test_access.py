import datetime

from django.http import HttpRequest
from django.test import TestCase, RequestFactory, override_settings, Client
from django.contrib.auth.models import User

from access_velocity.middleware import AccessVelocityMiddleware
from access_velocity.utils import lat_lon, get_distance, get_velocity
from access_velocity.conf import settings


class AccessTest(TestCase):
    VALID_USERNAME = 'valid-username'
    VALID_PASSWORD = 'valid-password'

    def setUp(self):
        """Create a valid user for login
        """
        self.user = User.objects.create_superuser(
            username=self.VALID_USERNAME,
            email='test@example.com',
            password=self.VALID_PASSWORD,
        )
        self.factory = RequestFactory()
        self.middleware = AccessVelocityMiddleware()

    def test_lat_lon(self):
        self.assertIsNone(lat_lon('127.0.0.1'))
        self.assertIsNone(lat_lon('0.0.0.0'))
        self.assertIsNone(lat_lon('asdf3?::[[[]]]fadsfs'))

        # dell.com (austin)
        lat,lon = lat_lon('dell.com')
        self.assertGreater(lat, 20)
        self.assertLess(lat, 40)
        self.assertGreater(lon, -105)
        self.assertLess(lon,-90)

    def test_distance(self):
        self.assertIsNone(get_distance('127.0.0.1', 'dell.com'))
        dst = get_distance('apple.com', 'dell.com')
        self.assertGreater(dst, 5000000)
        self.assertLess(dst, 5000000*2)

    def test_velocity(self):
        seconds = 10
        time1 = datetime.datetime.fromtimestamp(1284286794)
        time2 = datetime.datetime.fromtimestamp(1284286794 + seconds)

        velocity = get_velocity(500, time1, time2)
        self.assertEqual(velocity, 50)

        time2 = datetime.datetime.fromtimestamp(1284286794 + seconds + .04)
        velocity = get_velocity(500, time1, time2)
        self.assertLess(velocity, 50)

        with self.assertRaises(TypeError):
            get_velocity(None, time1, time2)

    def test_high_velocity(self):
        # not logged in is None
        request = self.factory.get('/admin/')
        response = self.middleware.process_view(request)
        self.assertIsNone(response)

        # localhost is None
        c = Client()
        c.login(username=self.VALID_USERNAME, password=self.VALID_PASSWORD)
        response = c.get('/admin/', REMOTE_ADDR='127.0.0.1')
        self.assertEqual(response.status_code, 200)

        response = c.get('/admin/', REMOTE_ADDR='143.166.135.105')
        response = c.get('/admin/', REMOTE_ADDR='17.172.224.47')
        self.assertEqual(response.status_code, 403)

