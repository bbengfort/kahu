# replicas.signals
# Singals used by replicas models - imported by apps.py
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Thu Jun 07 08:49:34 2018 -0400
#
# ID: signals.py [] benjamin@bengfort.com $

"""
Singals used by replicas models - imported by apps.py
"""

##########################################################################
## Imports
##########################################################################

import math
import secrets

from replicas import geoip
from .models import Replica
from .models import Latency

from rest_framework.authtoken.models import Token

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save


##########################################################################
## Replica Signals
##########################################################################

@receiver(pre_save, sender=Replica, dispatch_uid="replica_consistency_checks")
def replica_consistency_checks(sender, instance, *args, **kargs):
    """
    Performs consistency checks on the replica instance to ensure it's saved
    correctly. If fields are missing or incorrect, this signal updates the
    replica to ensure data is correctly saved.
    """

    # Ensure the replica has an associated API key
    if not instance.api_key:
        instance.api_key = secrets.token_urlsafe(32)

    # Create a unique name for the replica if it doesn't have one
    if not instance.name:
        instance.name = "{}-{}".format(instance.hostname, instance.precedence)

    # If no location or if IP address has changed, perform GeoIP lookup.
    if not instance.location or instance.tracker.has_changed('ip_address'):
        instance.location = geoip.lookup(instance.ip_address)


##########################################################################
## Latency Signals
##########################################################################

@receiver(pre_save, sender=Latency, dispatch_uid="recompute_latency_distribution")
def recompute_latency_distribution(sender, instance, *args, **kwargs):
    """
    Recomputes the aggregate statistics based on the cumulative figures stored
    in a latency row, ensuring it is always as up to date as possible.
    """
    N = float(instance.messages)
    S = instance.total

    if N > 0:
        instance.mean = S / N

    if N > 1:
        num = (N*instance.squares - S*S)
        den = (N * (N-1))
        instance.variance = num / den
        instance.stddev = math.sqrt(instance.variance)

    instance.range = instance.slowest - instance.fastest


##########################################################################
## User Signals
##########################################################################

@receiver(
    post_save,
    sender=settings.AUTH_USER_MODEL,
    dispatch_uid="assign_user_api_auth_token",
)
def assign_user_api_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
