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

from .models import Replica
from .utils import parse_bool, Health

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


ACTIVE = "active"
HEALTH = "health"


##########################################################################
## HTML Views
##########################################################################

class Replicas(LoginRequiredMixin, ListView):

    model = Replica
    paginate_by = 10
    template_name = "site/replicas.html"
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
        queryset = super(Replicas, self).get_queryset()
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
        context = super(Replicas, self).get_context_data(**kwargs)
        context['dashboard'] = 'replicas'
        context['replicas_type'] = self.get_queryset_title()
        return context
