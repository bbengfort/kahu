# replicas.serializers
# JSON serialization of replica model objects
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Fri Jun 08 13:36:22 2018 -0400
#
# ID: serializers.py [] benjamin@bengfort.com $

"""
JSON serialization of replica model objects
"""

##########################################################################
## Imports
##########################################################################

from .models import Replica
from rest_framework import serializers


##########################################################################
## Model Serializers
##########################################################################

class ReplicaSerializer(serializers.ModelSerializer):

    pid = serializers.IntegerField(source="precedence")
    ipaddr = serializers.IPAddressField(source="ip_address")

    class Meta:
        model = Replica
        fields = ("pid", "name", "address", "hostname", "ipaddr", "port")
        read_only_fields = ('address',)


##########################################################################
## API Serializers
##########################################################################

class HeartbeatSerializer(serializers.Serializer):

    ip_address = serializers.IPAddressField(allow_null=True)
