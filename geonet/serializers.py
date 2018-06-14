# geonet.serializers
# API serializers for geonet models.
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Thu Jun 14 11:29:44 2018 -0400
#
# ID: serializers.py [] benjamin@bengfort.com $

"""
API serializers for geonet models.
"""

##########################################################################
## Imports
##########################################################################

from .models import AWSInstance
from rest_framework import serializers


##########################################################################
## Model Serializers
##########################################################################

class AWSInstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = AWSInstance
        fields = ("instance_id", "instance_type", "availability_zone")
