# replicas.managers
# Query managers for replicas models.
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Thu Jun 07 09:01:15 2018 -0400
#
# ID: managers.py [] benjamin@bengfort.com $

"""
Query managers for replicas models.
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from datetime import timedelta

from .utils import Health, utcnow
from .utils import ONLINE_THRESHOLD, OFFLINE_THRESHOLD


##########################################################################
## Replica Manager
##########################################################################

class ReplicaQuerySet(models.QuerySet):

    def active(self):
        return self.filter(active=True)

    def health(self, status):
        if status == Health.UNKNOWN:
            return self.filter(last_seen=None)

        now = utcnow()

        if status == Health.ONLINE:
            threshold = timedelta(seconds=ONLINE_THRESHOLD)
            return self.filter(last_seen__gte=now-threshold)

        if status == Health.UNRESPONSIVE:
            return self.filter(last_seen__range=[
                now-timedelta(seconds=OFFLINE_THRESHOLD),
                now-timedelta(seconds=ONLINE_THRESHOLD)
            ])

        if status == Health.OFFLINE:
            threshold = timedelta(seconds=OFFLINE_THRESHOLD)
            return self.filter(last_seen__lt=now-threshold)

        raise ValueError("cannot filter health status '{}'".format(status))


class ReplicaManager(models.Manager):

    def get_queryset(self):
        return ReplicaQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def online(self):
        return self.get_queryset().health(Health.ONLINE)

    def unresponsive(self):
        return self.get_queryset().health(Health.UNRESPONSIVE)

    def offline(self):
        return self.get_queryset().health(Health.OFFLINE)
