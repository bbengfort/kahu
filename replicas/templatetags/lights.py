# replicas.templatetags.lights
# Status and health lights and filters
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Thu Jun 07 16:17:57 2018 -0400
#
# ID: lights.py [] benjamin@bengfort.com $

"""
Status and health lights and filters
"""

##########################################################################
## Imports
##########################################################################

from django import template
from replicas.utils import Health

# Register template tags
register = template.Library()


@register.inclusion_tag("snippets/light.html")
def active(replica):
    return {
        "title": "Status: Active" if replica.active else "Status: Inactive",
        "class": "text-success" if replica.active else "text-danger",
    }


@register.inclusion_tag("snippets/light.html")
def health(replica):
    status = replica.health()
    color = {
        Health.ONLINE: "success",
        Health.OFFLINE: "danger",
        Health.UNRESPONSIVE: "warning",
    }.get(status, "dark")

    context = {
        "title": "Health: {}".format(status.value.title()),
        "class": "text-{}".format(color),
    }

    return context


@register.inclusion_tag("snippets/light.html")
def instance_state(instance):
    state = instance.get('state', 'unknown')
    color = {
        'pending': "info",
        'running': "success",
        'shutting-down': "warning",
        'terminated': "secondary",
        'stopping': "warning",
        'stopped': "danger",
    }.get(state, "dark")

    context = {
        "title": "State: {}".format(state.title()),
        "class": "text-{}".format(color),
        "label": state, 
    }

    return context
