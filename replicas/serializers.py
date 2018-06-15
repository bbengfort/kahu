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
from geonet.models import AWSInstance
from geonet.serializers import AWSInstanceSerializer

from rest_framework import serializers


##########################################################################
## Model Serializers
##########################################################################

class ReplicaSerializer(serializers.ModelSerializer):

    pid = serializers.IntegerField(
        source="precedence", label="PID", required=False,
        help_text="the precedence of the replica in the cluster",
    )
    aws_instance = AWSInstanceSerializer(required=False, label="AWS Instance")

    class Meta:
        model = Replica
        fields = (
            "pid", "name", "description", "hostname",
            "ip_address", "domain", "port", "aws_instance",
        )
        read_only_fields = ('address',)

    def create(self, validated_data):
        # Pop the AWS-specific data off of the validated data
        aws_instance_data = validated_data.pop('aws_instance', None)

        # Create the replica object
        replica = Replica.objects.create(**validated_data)

        # Create the associated instance if it's given
        if aws_instance_data:
            aws_instance = AWSInstance.objects.create(
                replica=replica, **aws_instance_data
            )

        return replica


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


class ActivateSerializer(serializers.Serializer):

    active = serializers.BooleanField()
