# replicas.authentication
# Provides machine authentication to the API rather than user authentication.
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Fri Jun 08 12:42:32 2018 -0400
#
# ID: authentication.py [] benjamin@bengfort.com $

"""
Provides machine authentication to the API rather than user authentication.
"""

##########################################################################
## Imports
##########################################################################

from .models import Replica

from rest_framework import authentication
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import AuthenticationFailed


##########################################################################
## Machine User
##########################################################################

class MachineUser(AnonymousUser):

    def __init__(self, replica):
        self.replica = replica

    @property
    def is_authenticated(self):
        return True


##########################################################################
## Replica Authentication
##########################################################################

class ReplicaAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        api_key = request.META.get("HTTP_X_API_KEY", None)
        if not api_key:
            return None

        try:
            replica = Replica.objects.get(api_key=api_key)
        except Replica.DoesNotExist:
            raise AuthenticationFailed("Invalid API Key.")

        if not replica.active:
            raise AuthenticationFailed("Replica is inactive or not managed.")

        # Create a machine user with the device
        return (MachineUser(replica), api_key)
