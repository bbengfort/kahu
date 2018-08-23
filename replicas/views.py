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

from .authentication import MachineUser
from .models import Replica, Latency, SystemStatus
from .serializers import ReplicaSerializer, ActivateSerializer
from .serializers import HeartbeatSerializer, PingSerializer
from .serializers import LatencySerializer, NeighborSerializer
from .serializers import SystemStatusSerializer
from .permissions import IsMachineUser, IsActiveMachineUser
from .permissions import IsActiveMachineUserOrReadOnly
from .permissions import IsAdminOrReadOnly, IsMachineUserOrReadOnly
from .utils import parse_bool, Health, utcnow

from rest_framework import status
from rest_framework import viewsets
from rest_framework.reverse import reverse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from django.conf import settings
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import date

ACTIVE = "active"
HEALTH = "health"


##########################################################################
## HTML Views
##########################################################################

class ReplicaList(LoginRequiredMixin, ListView):

    model = Replica
    paginate_by = 20
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

class ReplicaViewSet(viewsets.ModelViewSet):
    """
    RESTful endpoint to manage replica objects on the system, accessed by
    GeoNet when creating or deleting instances from AWS.
    """

    serializer_class = ReplicaSerializer
    queryset = Replica.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly,)

    @action(detail=False, permission_classes=(IsAdminUser,))
    def tokens(self, request):
        """
        Admin users cen get a list of API tokens for all replicas for system
        configuration purposes.
        """
        data = self.get_queryset().values('name', 'api_key')
        return Response(data)

    @action(detail=True, methods=['post', 'put'], permission_classes=(IsAuthenticated,))
    def activate(self, request, pk=None):
        """
        From the user interface, activate and deactivate a replica.
        """
        replica = self.get_object()
        serializer = ActivateSerializer(data=request.data)
        if serializer.is_valid():
            if replica.active:
                if serializer.data['active']:
                    success = False
                    message = "replica {} already active"
                else:
                    success = True
                    message = "replica {} deactivated"
            else:
                if serializer.data['active']:
                    success = True
                    message = "replica {} activated"
                else:
                    success = False
                    message = "replica {} already inactive"

            replica.active = serializer.data['active']
            replica.save()
            return Response({
                "success": success, "message": message.format(replica.name)
            })
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get', 'post'], permission_classes=(IsAdminUser,))
    def geonet(self, request):
        """
        Reports the replica names that are active on GET and can set a group
        of replicas as active on POST (deactivating all others). Note that
        posting an empty list is equivalent to deactivating all replicas.
        """
        # TODO: Remove this method and find a better way to configure experiments! 
        if request.method == 'GET':
            data = Replica.objects.active().values_list("name", flat=True)
            return Response(data)

        if request.method == 'POST':
            names = list(map(str, request.data))
            pks = Replica.objects.filter(name__in=names).values_list("pk", flat=True)

            activated = Replica.objects.filter(id__in=pks).update(active=True)
            deactivated = Replica.objects.exclude(id__in=pks).update(active=False)
            return Response({"activated": activated, "deactivated": deactivated})

        # This should never happen
        return Response(status=status.HTTP_405_NOT_ALLOWED)

    def get_queryset(self):
        """
        Returns only active replicas on list.
        """
        queryset = super(ReplicaViewSet, self).get_queryset()
        if self.action == "list":
            queryset = queryset.active()
        return queryset


class HeartbeatViewSet(viewsets.ViewSet):
    """
    Purposefully lightweight liveness endpoint where replicas can report that
    they are online and functioning correctly. Only machines can access this
    endpoing, and it is POST only.
    """

    permission_classes = (IsAuthenticated, IsMachineUser, )

    def create(self, request):
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
            "replica": replica.name,
            "active": replica.active,
        })


class LatencyViewSet(viewsets.ViewSet):
    """
    Endpoint that handles ping reports from replicas. The neighbors detail
    action sends all active neighbors for the requesting replica to ping, then
    accepts ping latencies via POST. Autenticated users can read the list of
    all pairs of replicas and the computed latency between them.
    """

    permission_classes = (IsAuthenticated, IsActiveMachineUserOrReadOnly,)

    @action(detail=False, permission_classes=(IsActiveMachineUser,))
    def neighbors(self, request):
        """
        Returns the neighborhood of other replicas to ping for latency measures
        """
        replica = request.user.replica

        # For now, return all other unique IP addresses that are active.
        # TODO: return neighbors specific to source (e.g. by cluster).
        targets = Replica.objects.active().exclude(id=replica.id)
        serializer = NeighborSerializer(targets, many=True)
        return Response({"source": replica.name, "targets": serializer.data})

    def list(self, request):
        """
        Returns a list of the latency distributions for active replicas.
        """
        queryset = Latency.objects.filter(source__active=True)
        serializer = LatencySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        For all the pings posted, updates the distribution from the source.
        """
        replica = request.user.replica

        # Deserialize the request
        serializer = PingSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
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
        serializer = LatencySerializer(latencies, many=True)
        return Response(serializer.data)


class SystemHealthViewSet(viewsets.ViewSet):
    """
    Health check endpoint where replicas report the system status. Note that
    this is deliberately separate from the heartbeat to ensure that the liveness
    check is lightweight and not interrupted by system queries.
    """

    serializer_class = SystemStatusSerializer
    permission_classes = (IsAuthenticated, IsMachineUserOrReadOnly,)

    def list(self, request):
        """
        Returns a list of any replicas with recent status updates.
        """
        # Get system statuses that were modified today
        queryset = SystemStatus.objects.filter(modified__date=date.today())
        queryset = queryset.order_by('-modified').values("pk")

        # Create status URLs to the detail view
        status_urls = [
            reverse('api:health-detail', kwargs=kwargs, request=request)
            for kwargs in queryset
        ]

        return Response(status_urls)

    def create(self, request):
        """
        Replicas POST their health check statuses to the end point and are
        identified by their authentication details.
        """
        # Get the replica and check if it has an associated health status
        replica = request.user.replica
        created = False

        if not hasattr(replica, 'status'):
            SystemStatus.objects.create(replica=replica)
            created = True

        # Create the serializer and validate the incoming data
        serializer = SystemStatusSerializer(data=request.data)
        if serializer.is_valid():

            # Update the system status from the incoming data
            for key, val in serializer.validated_data.items():
                if val:
                    setattr(replica.status, key, val)
            replica.status.save()

            # Send the response back
            code = status.HTTP_201_CREATED if created else status.HTTP_204_NO_CONTENT
            return Response(None, status=code)

        # Return error messages from invalid request
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Returns the replica status if it exists, or raises a 404 if not created.
        """
        try:
            health = SystemStatus.objects.get(pk=pk)
        except SystemStatus.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(health)
        return Response(serializer.data)
