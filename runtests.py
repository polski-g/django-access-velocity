#!/usr/bin/env python

from __future__ import unicode_literals

import os
import sys

import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test.utils import get_runner


def run_tests():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'access_velocity.test_settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['access_velocity.tests'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests()
