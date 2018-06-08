# replicas.exceptions
# Exceptions and API exceptions for the replicas app.
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Fri Jun 08 14:52:16 2018 -0400
#
# ID: exceptions.py [] benjamin@bengfort.com $

"""
Exceptions and API exceptions for the replicas app.
"""

##########################################################################
## Imports
##########################################################################

from rest_framework.exceptions import APIException


##########################################################################
## API Exceptions
##########################################################################

class ReplicaEndpointOnly(APIException):

    status_code = 403
    default_detail = 'only active replicas may access this endpoint'
    default_code = 'replica_endpoint_only'
