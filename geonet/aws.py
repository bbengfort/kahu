# geonet.aws
# AWS/Boto3 helper functions and utilities
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Mon Jun 11 08:23:11 2018 -0400
#
# ID: aws.py [] benjamin@bengfort.com $

"""
AWS/Boto3 helper functions and utilities
"""

##########################################################################
## Imports
##########################################################################

import boto3
import asyncio

from django.conf import settings
from geonet.models import BotoCache, RegionCache


##########################################################################
## AWS Regions
##########################################################################

AWS_REGIONS = {
    "virginia": "us-east-1",
    "ohio": "us-east-2",
    "california": "us-west-1",
    "oregon": "us-west-2",
    "canada": "ca-central-1",
    "tokyo": "ap-northeast-1",
    "seoul": "ap-northeast-2",
    "singapore": "ap-southeast-1",
    "sydney": "ap-southeast-2",
    "mumbai": "ap-south-1",
    "frankfurt": "eu-central-1",
    "ireland": "eu-west-1",
    "london": "eu-west-2",
    "paris": "eu-west-3",
    "brazil": "sa-east-1",
}

AWS_LOCATIONS = {v: k for k,v in AWS_REGIONS.items()}


##########################################################################
## Connect to AWS utility by region
##########################################################################

def connect(region, service="ec2", **kwargs):
    """
    Create a boto3 client that is connected to the specified region. Pass any
    arguments to the boto3.ec2.connect_to_region function. Default values for
    the kwargs will be collected from the Django settings.
    """
    # Lookup region by locale name if required
    if region.lower() in AWS_REGIONS:
        region = AWS_REGIONS[region.lower()]

    # Create default options
    options = {
        "service_name": service,
        "region_name": region,
        "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
    }

    # Override defaults with user defined values
    options.update(kwargs)
    return boto3.client(**options)


##########################################################################
## Generic Operations
##########################################################################

async def apply(operation, conn, **kwargs):
    """
    Apply the given operation to the connection with the specified arguments,
    then cache the result to the database; updating modified timestamps.
    """
    # Raises exception if unknown operation (must be called before db ops)
    func = getattr(conn, operation)

    # Fetch the operation caches from the database
    cache, _ = BotoCache.objects.get_or_create(operation=operation)
    region_cache, _ = cache.regions.get_or_create(region=conn.meta.region_name)

    # Apply the operation and cache it
    try:
        region_cache.cache = func(**kwargs)
        region_cache.error = ""
    except Exception as e:
        region_cache.cache = None
        region_cache.error = str(e)

    # Save the caches (and update timestamps, etc)
    cache.save()
    region_cache.save()


def apply_to_regions(operation, regions=AWS_REGIONS.values(), **kwargs):
    """
    Apply the operation to all regions asynchronously, waiting for all
    requests to complete before exiting.
    """
    # TODO: allow regions to be an iterable of connections or establish a
    # connection to the region if a string is passed in.
    conns = [connect(region) for region in regions]

    # Create a new loop to avoid no current event loop errors
    # TODO: is this a bad idea?
    loop  = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Note the expansion * of the apply operations being gathered (required).
    loop.run_until_complete(asyncio.gather(*[
        apply(operation, conn, **kwargs) for conn in conns
    ]))
    loop.close()
