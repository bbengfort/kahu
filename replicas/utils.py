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


##########################################################################
## Enumerations
##########################################################################

class Health(Enum):

    UNKNOWN = "unknown"
    ONLINE  = "online"
    OFFLINE = "offline"
    UNRESPONSIVE = "unresponsive"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
