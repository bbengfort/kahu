# kahu.views
# Default application views for the application
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Wed Jun 06 16:30:19 2018 -0400
#
# ID: views.py [] benjamin@bengfort.com $

"""
Default application views for the application
"""

##########################################################################
## Imports
##########################################################################

import kahu
import json

from datetime import datetime

from replicas.models import Location

from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


##########################################################################
## Views
##########################################################################

class Overview(LoginRequiredMixin, TemplateView):

    template_name = "site/overview.html"

    def get_context_data(self, **kwargs):
        context = super(Overview, self).get_context_data(**kwargs)
        context['dashboard'] = 'overview'
        context['google_maps_api'] = settings.GOOGLE_MAPS_API_KEY

        markers = []
        for location in Location.objects.all():
            markers.append({
                "lat": float(location.latitude),
                "lng": float(location.longitude),
                "title": location.location,
                "replicas": [
                    replica.hostname for replica in location.replicas.all()
                ]
            })

        context['markers'] = json.dumps(markers)
        return context


##########################################################################
## API Views
##########################################################################

class HeartbeatViewSet(viewsets.ViewSet):
    """
    Endpoint for heartbeat checking, includes status and version.
    """

    permission_classes = [AllowAny]

    def list(self, request):
        return Response({
            "status": "ok",
            "version": kahu.get_version(),
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        })
