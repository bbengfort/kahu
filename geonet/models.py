# geonet.models
# Nodels for the geonet app
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Mon Jun 11 08:10:28 2018 -0400
#
# ID: models.py [] benjamin@bengfort.com $

"""
Models for the geonet app
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder


##########################################################################
## Boto Cache Models
##########################################################################

class BotoCache(TimeStampedModel):
    """
    A Boto cache maps a single boto operation to multiple region caches, which
    in turn contain the data response from AWS in a JSON field. This top level
    cache object is the thing that is "updated" periodically.
    """

    operation = models.CharField(
        max_length=255, null=False, blank=False, unique=True,
        help_text="unique name of the boto operation being cached"
    )

    class Meta:
        db_table = "boto_cache"
        get_latest_by = "modified"

    def __str__(self):
        return self.operation


class RegionCache(TimeStampedModel):
    """
    Caches the AWS response for an operation (identified by BotoCache), on a
    per-region basis. The data itself is stored on this field.
    """

    region = models.CharField(
        max_length=255, null=False, blank=False,
        help_text="name of the region the request was made to",
    )
    operation = models.ForeignKey(
        "geonet.BotoCache", null=False, blank=False,
        on_delete=models.CASCADE, related_name='regions',
        help_text="the associated operation the data is being stored for",
    )
    cache = JSONField(
        encoder=DjangoJSONEncoder, null=True, blank=True, editable=False,
        help_text="the actual cached data from the Boto3 response",
    )
    error = models.CharField(
        max_length=255, null=True, blank=True, editable=False, default="",
        help_text="any error or exception raised during the operation"
    )

    class Meta:
        db_table = "boto_region_cache"
        get_latest_by = "modified"
        unique_together = ("region", "operation")

    @property
    def success(self):
        return not self.error

    def __str__(self):
        return "{} ← {}".format(self.region, self.operation)
