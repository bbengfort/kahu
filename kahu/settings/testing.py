# kahu.settings.testing
# Testing settings to enable testing on Travis with Django tests.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Jun 06 16:28:36 2018 -0400
#
# ID: testing.py [] benjamin@bengfort.com $

"""
Testing settings to enable testing on Travis with Django tests.
"""

##########################################################################
## Imports
##########################################################################

import os
from .base import *

##########################################################################
## Test Settings
##########################################################################

## Hosts
ALLOWED_HOSTS    = ['localhost', '127.0.0.1']

## Database Settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': environ_setting('DB_NAME', 'kahu'),
        'USER': environ_setting('DB_USER', 'postgres'),
        'PASSWORD': environ_setting('DB_PASS', ''),
        'HOST': environ_setting('DB_HOST', 'localhost'),
        'PORT': environ_setting('DB_PORT', '5432'),
    },
}

STATICFILES_STORAGE =  'django.contrib.staticfiles.storage.StaticFilesStorage'

## Content without? side effects
MEDIA_ROOT         = "/tmp/kahu/media"
STATIC_ROOT        = "/tmp/kahu/static"

##########################################################################
## Django REST Framework
##########################################################################

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
)
