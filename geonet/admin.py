# geonet.admin
# Admin registration for the geonet app
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Mon Jun 11 08:10:28 2018 -0400
#
# ID: admin.py [] benjamin@bengfort.com $

"""
Admin registration for the geonet app
"""

##########################################################################
## Imports
##########################################################################

from .models import AWSInstance
from django.contrib import admin

##########################################################################
## Register your models here
##########################################################################

admin.site.register(AWSInstance)
