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

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


##########################################################################
## HTML Views
##########################################################################

class Replicas(LoginRequiredMixin, TemplateView):

    template_name = "site/replicas.html"

    def get_context_data(self, **kwargs):
        context = super(Replicas, self).get_context_data(**kwargs)
        context['dashboard'] = 'replicas'
        return context
