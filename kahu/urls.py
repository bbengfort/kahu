# kahu.urls
# Kahu URL configuration
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Wed Jun 06 16:16:16 2018 -0400
#
# ID: urls.py [] benjamin@bengfort.com $

"""
Kahu URL configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from rest_framework import routers
from django.urls import path, include

from kahu.views import *
from replicas.views import *


##########################################################################
## Endpoint Discovery
##########################################################################

router = routers.DefaultRouter()
router.register(r'status', StatusViewSet, "status")


##########################################################################
## URL Patterns
##########################################################################

urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),

    # Application URLs
    path('', Overview.as_view(), name="overview"),
    path('replicas/', Replicas.as_view(), name="replicas"),

    # Authentication URLs
    path('user/', include(('social_django.urls', 'social_django'), namespace='social')),
    path('user/', include('django.contrib.auth.urls')),

    ## REST API Urls
    path('api/', include((router.urls, 'rest_framework'), namespace="api")),
]
