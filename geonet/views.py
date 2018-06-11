# geonet.views
# Views for the geonet app
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Mon Jun 11 08:10:28 2018 -0400
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views for the geonet app
"""

##########################################################################
## Imports
##########################################################################

from geonet import aws
from geonet.models import BotoCache

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


##########################################################################
## AWS Status View
##########################################################################

class AWSStatus(LoginRequiredMixin, TemplateView):

    operation = "describe_instances"
    template_name = "site/geonet.html"

    def post(self, request, *args, **kwargs):
        """
        Refresh the AWS instance list when a request is posted.
        """
        aws.apply_to_regions(self.operation)
        redirect_url = reverse('geonet')
        return HttpResponseRedirect(redirect_url)

    def get_context_data(self, **kwargs):
        """
        Called from a GET request -- display instances from the cache.
        """
        context = super(AWSStatus, self).get_context_data(**kwargs)
        context['dashboard'] = 'geonet'

        context.update(self.get_aws_status())

        return context

    def get_boto_cache(self):
        """
        Lookup the last describe instances operation or return None
        """
        try:
            return BotoCache.objects.get(operation=self.operation)
        except BotoCache.DoesNotExist:
            return None

    def get_aws_status(self):
        """
        Extract the AWS status to add to the context
        """
        # Default status
        status = {
            'modified': 'never',
            'instances': [],
        }

        # Load the cache and return if no cache exists
        cache = self.get_boto_cache()
        if cache is None:
            return status

        # Update modified from the cache and instances from the regions
        status['modified'] = cache.modified
        status['instances'] = list(self._parse_instances_json(cache))
        status['num_instances'] = len(status['instances'])
        status['num_regions'] = cache.regions.count()
        return status

    def _parse_instances_json(self, cache):
        """
        Parse instance details from the cache JSON to display
        """
        for region in cache.regions.all():
            for reservation in region.cache.get('Reservations', []):
                for instance in reservation.get('Instances', []):
                    name = None
                    for tag in instance["Tags"]:
                        if tag["Key"].lower() == "name":
                            name = tag["Value"]
                            break

                    yield {
                        "name": name,
                        "state": instance["State"]["Name"],
                        "location": aws.AWS_LOCATIONS[region.region],
                        "zone": instance["Placement"]["AvailabilityZone"],
                        "instance": instance["InstanceId"],
                        "type": instance["InstanceType"],
                        "ip_address": instance.get("PublicIpAddress", None),
                    }
