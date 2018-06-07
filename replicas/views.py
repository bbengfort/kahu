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
from .utils import parse_bool

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


##########################################################################
## HTML Views
##########################################################################

class Replicas(LoginRequiredMixin, ListView):

    model = Replica
    paginate_by = 10
    template_name = "site/replicas.html"
    context_object_name = "replicas"

    def get_queryset(self):
        queryset = super(Replicas, self).get_queryset()

        active = self.request.GET.get('active', None)
        if active is not None:
            active = parse_bool(active)
            queryset = queryset.filter(active=active)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(Replicas, self).get_context_data(**kwargs)
        context['dashboard'] = 'replicas'
        return context
