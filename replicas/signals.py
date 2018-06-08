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

from .models import Replica
from .models import Latency

from django.dispatch import receiver
from django.db.models.signals import pre_save


##########################################################################
## Replica Signals
##########################################################################

@receiver(pre_save, sender=Replica, dispatch_uid="create_replica_api_key")
def create_replica_api_key(sender, instance, *args, **kargs):
    """
    Creates an API Key for the replica if it doesn't already have one.
    """
    if not instance.api_key:
        instance.api_key = secrets.token_urlsafe(32)


@receiver(pre_save, sender=Replica, dispatch_uid="create_replica_unique_name")
def create_replica_unique_name(sender, instance, *args, **kargs):
    """
    Creates a unique name for the replica if it doesn't already have one.
    """
    if not instance.name:
        instance.name = "{}-{}".format(instance.hostname, instance.precedence)



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
