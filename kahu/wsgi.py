# kahu.wsgi
# WSGI config for Kahu project.
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Wed Jun 06 16:16:57 2018 -0400
#
# ID: wsgi.py [] benjamin@bengfort.com $

"""
WSGI config for kahu project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

##########################################################################
## Imports
##########################################################################

import os
import dotenv

from django.core.wsgi import get_wsgi_application

##########################################################################
## WSGI Configuration
##########################################################################

# load .env file
dotenv.load_dotenv(dotenv.find_dotenv())

# set default environment variables
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kahu.settings.development")

# export the wsgi application for import
application = get_wsgi_application()
