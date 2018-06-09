# replicas.views
# Controllers and views for the replicas app (HTML/JSON)
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Wed Jun 06 22:18:28 2018 -0400
#
# ID: views.py [] benjamin@bengfort.com $

"""
Controllers and views for the replicas app (HTML/JSON)
"""

##########################################################################
## Imports
##########################################################################

from .models import Replica, Latency
from .authentication import MachineUser
from .serializers import PingSerializer
from .serializers import ReplicaSerializer
from .serializers import HeartbeatSerializer
from .serializers import LatencySerializer
from .exceptions import ReplicaEndpointOnly
from .utils import parse_bool, Health, utcnow

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from django.conf import settings
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


ACTIVE = "active"
HEALTH = "health"


##########################################################################
## HTML Views
##########################################################################

class ReplicaList(LoginRequiredMixin, ListView):

    model = Replica
    paginate_by = 10
    template_name = "site/replica_list.html"
    context_object_name = "replicas"

    def parse_query_string(self):
        params = {}

        active = self.request.GET.get(ACTIVE, None)
        if active is not None:
            params[ACTIVE] = parse_bool(active)

        health = self.request.GET.get(HEALTH, None)
        if health is not None:
            params[HEALTH] = Health(health)

        return params

    def get_queryset(self):
        queryset = super(ReplicaList, self).get_queryset()
        params = self.parse_query_string()

        if ACTIVE in params:
            queryset = queryset.filter(active=params[ACTIVE])

        if HEALTH in params:
            queryset = queryset.active().health(params[HEALTH])

        return queryset

    def get_queryset_title(self):
        params = self.parse_query_string()

        if HEALTH in params:
            return params[HEALTH].value

        if ACTIVE in params:
            return "active" if params[ACTIVE] else "inactive"

        return "all"

    def get_context_data(self, **kwargs):
        context = super(ReplicaList, self).get_context_data(**kwargs)
        context['dashboard'] = 'replicas'
        context['replicas_type'] = self.get_queryset_title()
        return context


class ReplicaDetail(LoginRequiredMixin, DetailView):

    model = Replica
    slug_field = "name"
    template_name = "site/replica_detail.html"
    context_object_name = "replica"

    def get_context_data(self, **kwargs):
        context = super(ReplicaDetail, self).get_context_data(**kwargs)
        context['google_maps_api'] = settings.GOOGLE_MAPS_API_KEY
        context['dashboard'] = 'replicas'
        return context


##########################################################################
## API Views
##########################################################################

class ReplicaViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ReplicaSerializer
    queryset = Replica.objects.active()


class HeartbeatViewSet(viewsets.ViewSet):

    def create(self, request):
        # Validate replica via machine user
        if not isinstance(request.user, MachineUser):
            raise ReplicaEndpointOnly("only replicas can post heartbeats")

        # Fetch the replica and update the last seen timestamp
        replica = request.user.replica
        replica.last_seen = utcnow()

        # Deserialize the request
        serializer = HeartbeatSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        # Permit an update to the IP address, our version of DDNS
        data = serializer.validated_data
        if data.get("ip_address", None):
            replica.ip_address = data["ip_address"]

        # Update the hostname (in case the replica process executes on a new host)
        if data.get("hostname", None):
            replica.hostname = data["hostname"]

        # Save the updates to the replica
        replica.save()

        return Response({
            "success": True,
            "replica": replica.hostname,
            "ipaddr": replica.ip_address,
            "active": replica.active,
        })


class LatencyViewSet(viewsets.ViewSet):

    def validate_replica(self, request):
        if not isinstance(request.user, MachineUser):
            raise ReplicaEndpointOnly(
                "only replicas can post latencies and request neighbors"
            )

        return request.user.replica

    def list(self, request):
        """
        Returns the neighborhood of other replicas to ping for latency measures
        """
        replica = self.validate_replica(request)

        # For now, return all other unique IP addresses
        # TODO: make this better
        neighbors = Replica.objects.active().exclude(id=replica.id)
        neighbors = [
            {
                "hostname": neighbor.name,
                "state": neighbor.health().value,
                "addr": str(neighbor.ip_address),
                "dns": neighbor.domain,
            }
            for neighbor in neighbors
        ]

        return Response({
            "source": replica.hostname,
            "targets": neighbors,
        })


    def create(self, request):
        """
        For all the pings posted, updates the distribution from the source.
        """
        replica = self.validate_replica(request)

        # Deserialize the request
        serializer = PingSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(
                serializers.errors, status=status.HTTP_400_BAD_REQUEST
            )

        latencies = []
        for ping in serializer.validated_data:
            target = Replica.objects.get(name=ping['target'])
            latency, _ = Latency.objects.get_or_create(
                source=replica, target=target
            )

            latencies.append(Latency.update_from_ping(
                latency.id, ping['latency'], ping['timeout'])
            )

        # Serialize the response
        serializer = LatencySerializer(data=latencies, many=True)
        serializer.is_valid()
        return Response(serializer.data)
