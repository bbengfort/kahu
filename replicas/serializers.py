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

from .models import Replica, Latency
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


class NeighborSerializer(serializers.ModelSerializer):

    state = serializers.SerializerMethodField()

    class Meta:
        model = Replica
        fields = ("name", "state", "ip_address", "domain")

    def get_state(self, obj):
        return obj.health().value


class LatencySerializer(serializers.ModelSerializer):

    source = serializers.SlugRelatedField(slug_field="name", read_only=True)
    target = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Latency
        fields = (
            "source", "target", "messages", "timeouts", "fastest",
            "slowest", "mean", "stddev", "range"
        )


##########################################################################
## API Serializers
##########################################################################

class HeartbeatSerializer(serializers.Serializer):

    hostname = serializers.CharField(max_length=255, allow_blank=True)
    ip_address = serializers.IPAddressField(allow_blank=True)


class PingSerializer(serializers.Serializer):

    target = serializers.CharField()
    latency = serializers.FloatField()
    timeout = serializers.BooleanField()
