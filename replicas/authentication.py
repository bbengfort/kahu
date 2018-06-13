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

class KahuTokenAuthentication(authentication.TokenAuthentication):
    """
    Provides simple token authentication for both users and machine clients to
    the API by looking up both user tokens as drf.TokenAuthentication does, and
    falling back to looking up replicas by API_KEY if that fails.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a

    Ensure that HTTPS is used in production with this authentication.
    """

    keyword = "Bearer"

    def authenticate_credentials(self, key):
        """
        First look up a machine user by key, otherwise call super to return a
        human user's authentication key.
        """
        try:
            # Find a replica by its API Key
            replica = Replica.objects.get(api_key=key)

            # NOTE: do not do active check on replica, so inactive replicas
            # can still post heartbeat messages; this is a permission. 

            # Create a machine user with the device and return it
            # TODO: key should be a token object, works for now
            return (MachineUser(replica), key)
        except Replica.DoesNotExist:
            # Default to standard user authentication
            return super(KahuTokenAuthentication, self).authenticate_credentials(key)
