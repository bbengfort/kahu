# replicas.utils
# Utilities and constant enumerations
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Thu Jun 07 13:57:11 2018 -0400
#
# ID: utils.py [] benjamin@bengfort.com $

"""
Utilities and constant enumerations
"""

##########################################################################
## Imports
##########################################################################

from enum import Enum
from datetime import datetime
from django.utils.timezone import utc


##########################################################################
## Helpers
##########################################################################

def parse_bool(val):
    if isinstance(val, str):
        val = val.lower()

        if val.startswith('t'):
            return True
        if val.startswith('f'):
            return False

        val = int(val)

    return bool(val)


def utcnow():
    return datetime.now(utc)


##########################################################################
## Enumerations
##########################################################################

ONLINE_THRESHOLD = 300
OFFLINE_THRESHOLD = 3600


class Health(Enum):

    UNKNOWN = "unknown"
    ONLINE  = "online"
    OFFLINE = "offline"
    UNRESPONSIVE = "unresponsive"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
