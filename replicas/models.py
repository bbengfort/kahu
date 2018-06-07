# replicas.models
# Database models for the replicas app.
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Wed Jun 06 22:20:21 2018 -0400
#
# ID: models.py [] benjamin@bengfort.com $

"""
Database models for the replicas app.
"""

##########################################################################
## Imports
##########################################################################

from django.db import models

from model_utils.models import TimeStampedModel


##########################################################################
##  Replica Object
##########################################################################

class Replica(TimeStampedModel):
    """
    A replica represents a single distributed process running on a host machine
    managed by Kahu. Unlike previous versions of Kahu, there is no disambiguation
    between machine and replica (so if multiple processes are running on the
    same machine, there will be data duplication). However, because for the
    most part there is a one-to-one relationship between replica process and
    host machine (particularly when running on virtual instances in the cloud),
    this duplication is acceptable.
    """

    hostname = models.CharField(
        max_length=255, null=False, blank=False,
        help_text="unique identifying name of the host"
    )
    active = models.BooleanField(
        default=True,
        help_text="the replica is currently under management"
    )
    precedence = models.PositiveSmallIntegerField(
        default=0, blank=True,
        help_text="the precedence of the replica over other replicas"
    )
    domain = models.CharField(
        max_length=255, null=True, blank=True, default="",
        help_text="domain name for the specified host if supplied"
    )
    ip_address = models.GenericIPAddressField(
        null=False, blank=False,
        help_text="the IP address replicas can connect to"
    )
    port = models.IntegerField(
        default=3264, blank=False, null=False,
        help_text="the port the replica is listening for consensus on"
    )
    location = models.ForeignKey(
        'replicas.Location', null=True, blank=True,
        on_delete=models.PROTECT, related_name='replicas',
        help_text="the GeoIP location of the replica",
    )
    last_seen = models.DateTimeField(
        editable=False, null=True,
        help_text="the time of the last ping from the replica"
    )
    api_key = models.CharField(
        max_length=45, null=False, editable=False, unique=True,
        help_text="generated API key that identifies a host"
    )

    class Meta:
        db_table = "replicas"
        get_latest_by = "last_seen"
        ordering = ("precedence", "last_seen")


    def __str__(self):
        return "{} ({}:{})".format(self.hostname, self.ipaddr, self.port)


##########################################################################
## GeoIP Location
##########################################################################

class Location(TimeStampedModel):
    """
    Represents a location created by a GeoIP lookup, associated with the
    location of the replica's IP Address. These are combined into a normalized
    table because we expect many replicas to be colocated.
    """

    location = models.CharField(
        max_length=255, null=True, blank=True, default="",
        help_text="text description of the location (e.g. city, state)"
    )
    latitude = models.DecimalField(
        max_digits=10, decimal_places=6, null=False, blank=False,
        help_text="latitude of the location"
    )
    longitude = models.DecimalField(
        max_digits=10, decimal_places=6, null=False, blank=False,
        help_text="longitude of the location"
    )

    class Meta:
        db_table = "locations"
        get_latest_by = "modified"
        unique_together = ("latitude", "longitude")


    def __str__(self):
        if self.location:
            return self.location
        return "{}, {}".format(self.latitude, self.longitude)


##########################################################################
## Ping Latencies
##########################################################################

class Latency(TimeStampedModel):
    """
    Stores an online computation of the distribution of latencies between two
    replicas over time. The distribution can be updated by a single ping delay
    and all distributed statistics will be recomputed.
    """

    source = models.ForeignKey(
        'replicas.Replica', null=False, blank=False,
        on_delete=models.CASCADE, related_name='latencies',
        help_text="the replica where the ping originates",
    )
    target = models.ForeignKey(
        'replicas.Replica', null=False, blank=False,
        on_delete=models.CASCADE, related_name='+',
        help_text="the target of the ping to measure RTT to",
    )
    messages = models.BigIntegerField(
        default=0, null=False, blank=False,
        help_text="the number of successful pings (excludes timeouts)"
    )
    timeouts = models.BigIntegerField(
        default=0, null=False, blank=False,
        help_text="the number of unsuccessful pings"
    )
    total = models.FloatField(
        default=0.0, null=False, blank=False,
        help_text="the sum of all latencies in milliseconds"
    )
    squares = models.FloatField(
        default=0.0, null=False, blank=False,
        help_text="the sum of all latencies squared in milliseconds"
    )
    fastest = models.FloatField(
        default=0.0, null=False, blank=False,
        help_text="the minimum latency in milliseconds"
    )
    slowest = models.FloatField(
        default=0.0, null=False, blank=False,
        help_text="the maximum latency in milliseconds"
    )
    mean = models.FloatField(
        default=0.0, null=False, editable=False,
        help_text="the computed latency mean in milliseconds"
    )
    stddev = models.FloatField(
        default=0.0, null=False, editable=False,
        help_text="the computed latency standard deviation in milliseconds"
    )
    variance = models.FloatField(
        default=0.0, null=False, editable=False,
        help_text="the computed latency variance in milliseconds"
    )
    range = models.FloatField(
        default=0.0, null=False, editable=False,
        help_text="the computed latency range in milliseconds"
    )

    class Meta:
        db_table = "latencies"
        get_latest_by = "modified"
        unique_together = ("source", "target")
        verbose_name_plural = "latencies"


    def __str__(self):
        return "{} ⇄ {} μ={:0.3f}ms σ={:0.3f}ms"