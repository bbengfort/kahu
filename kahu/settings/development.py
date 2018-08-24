# kahu.settings.development
# Configuration for the development environment.
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Wed Jun 06 16:27:00 2018 -0400
#
# ID: development.py [] benjamin@bengfort.com $

"""
Configuration for the development environment.
"""

##########################################################################
## Imports
##########################################################################

import os
from .base import *


##########################################################################
## Development Environment
##########################################################################

ALLOWED_HOSTS = ('127.0.0.1', 'localhost')

MEDIA_ROOT = os.path.join(PROJECT, 'media')

## Static files served by WhiteNoise nostatic server
STATIC_ROOT = os.path.join(PROJECT, 'tmp', 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
