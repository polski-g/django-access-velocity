#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import codecs
from setuptools import setup, find_packages

from access_velocity import get_version

setup(
    name='django-access-velocity',
    version=get_version(),
    description='Ensure that a registered user is not trying to bot-net your application',
    long_description=(codecs.open('README.txt', encoding='utf-8').read()),
    keywords='authentication django security'.split(),
    url='https://github.com/polski-g/django-access-velocity',
    license='LGPL-3.0',
    package_dir={'access_velocity': 'access_velocity'},
    install_requires=[
        'geoip2',
        'geopy',
        'django-appconf',
        'django-ipware',
    ],
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: Log Analysis',
        'Topic :: Security',
        'Topic :: System :: Logging',
    ],
    zip_safe=False,
)
