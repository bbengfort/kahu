# replicas.admin
# Admin management for replicas models
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Wed Jun 06 22:19:17 2018 -0400
#
# ID: admin.py [] benjamin@bengfort.com $

"""
Admin management for replicas models
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from .models import Replica, Location, Latency


##########################################################################
## Register your models here
##########################################################################

admin.site.register(Replica)
admin.site.register(Location)
admin.site.register(Latency)
