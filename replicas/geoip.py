# replicas.geoip
# GeoIP Lookup from MaxMind service
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Sat Jun 09 10:41:24 2018 -0400
#
# ID: geoip.py [] benjamin@bengfort.com $

"""
GeoIP Lookup from MaxMind service
"""

##########################################################################
## Imports
##########################################################################

import requests

from .models import Location

from django.conf import settings
from requests.auth import HTTPBasicAuth


##########################################################################
## GeoIP API Class
##########################################################################

class GeoIP(object):
    """
    A wrapper around the MaxMind API to lookup geographies based on IP address.
    """

    BASE_URI = "https://geoip.maxmind.com"

    def __init__(self, username, password):
        self.auth = HTTPBasicAuth(username, password)

    def __call__(self, ipaddr):
        return self.lookup(ipaddr)

    def lookup(self, ipaddr):
        """
        Performs a GeoIP lookup for the specified IP Address, then returns a
        location object from the database.
        """
        # TODO: Generalize endpoint construction
        endpoint = "{}/geoip/v2.1/city/{}".format(self.BASE_URI, ipaddr)
        resp = requests.get(endpoint, auth=self.auth)
        return self.parse(resp.json())

    def parse(self, data):
        """
        Parses the MaxMind API GeoIP response and gets or creates a location
        object from the database.
        """
        location = {
            "latitude": data["location"]["latitude"],
            "longitude": data["location"]["longitude"],
        }

        # Get or create the location from the database
        location, created = Location.objects.get_or_create(**location)

        # If the location is created, extract the location name.
        if created:
            try:
                location = self._parse_locale(location, data)
            except Exception as e:
                # Failure to perform locale parsing should not cause a 500 error
                # TODO: add logging functionality to report failures
                pass

        return location

    def _parse_locale(self, location, data):
        """
        Sets the locale to City, State if in the US otherwise City, Country.
        """
        city = data["city"]["names"]["en"]

        if data["country"]["iso_code"] == "US":
            state = data["subdivisions"][0]["names"]["en"]
        else:
            state = data["country"]["names"]["en"]

        # Update the location in the database
        location.location = "{}, {}".format(city, state)
        location.save()

        return location


##########################################################################
## Default Lookup Function
##########################################################################

lookup = GeoIP(settings.GEOIP2_API_USER, settings.GEOIP2_API_KEY)
