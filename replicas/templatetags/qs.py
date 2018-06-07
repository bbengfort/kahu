# replicas.templatetags.qs
# Query string helper tags
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Thu Jun 07 17:44:01 2018 -0400
#
# ID: qs.py [] benjamin@bengfort.com $

"""
Query string helper tags
"""

##########################################################################
## Imports
##########################################################################

from django import template

# Register template tags
register = template.Library()


@register.simple_tag
def query_string(field, value, urlencode=None):
    parts = ["{}={}".format(field, value)]
    if urlencode:
        query = urlencode.split('&')
        query = list(filter(lambda p: p.split('=')[0] != field, query))
        parts.extend(query)

    return "?{}".format("&".join(parts))
