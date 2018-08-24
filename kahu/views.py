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

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style('darkgrid')
sns.set_context('notebook')

from datetime import datetime

from replicas.models import Replica
from replicas.models import Location, Latency

from django.views import View
from django.conf import settings
from django.http import HttpResponse
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
        context['status'] = {
            "active": Replica.objects.active().count(),
            "online": Replica.objects.online().active().count(),
            "unresponsive": Replica.objects.unresponsive().active().count(),
            "offline": Replica.objects.offline().active().count(),
        }

        markers = []
        for location in Location.objects.all():
            if location.replicas.active().count() > 0:
                markers.append(location.get_marker())

        context['markers'] = json.dumps(markers)
        return context


class LatencyDetail(LoginRequiredMixin, TemplateView):

    template_name = "site/latency.html"

    def get_context_data(self, **kwargs):
        context = super(LatencyDetail, self).get_context_data(**kwargs)
        context['dashboard'] = 'latency'

        return context


class GlobalLatencySVG(LoginRequiredMixin, View):

    def get(self, request):
        figure, ax = plt.subplots()

        latency = Latency.objects.filter(source__name__startswith="alia").order_by('source__name').values('source__name', 'target__name', 'mean')
        import pandas as pd
        df = pd.DataFrame(list(latency)).pivot('source__name', 'target__name', 'mean')
        sns.heatmap(ax=ax, data=df, cmap="RdYlGn_r")

        figure.set_dpi(72)
        figure.set_size_inches(12, 12)
        figure.set_tight_layout(True)

        from io import StringIO
        image_data = StringIO()
        figure.savefig(image_data, format="svg")
        image_data.seek(0)

        return HttpResponse(image_data.read(), content_type="image/svg+xml")


##########################################################################
## API Views
##########################################################################

class StatusViewSet(viewsets.ViewSet):
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
