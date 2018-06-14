# replicas.permissions
# Custom permissions for replica clients of the API
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Wed Jun 13 08:06:08 2018 -0400
#
# ID: permissions.py [] benjamin@bengfort.com $

"""
Custom permissions for replica clients of the API
"""

##########################################################################
## Imports
##########################################################################

from .authentication import MachineUser
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    """
    Allow admins to POST/PUT/DELETE and all other authenticated users to GET.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super(IsAdminOrReadOnly, self).has_permission(request, view)


class IsMachineUser(permissions.BasePermission):
    """
    Allow a machine user to access this resource, but not a human user.

    Note that to allow both machine and human users, simply use the default
    IsAuthenticated permisison, since MachineUsers are authenticated.
    """

    message = "only replica clients have access permission to this resource"

    def has_permission(self, request, view):
        return request.user and self.is_machine(request.user)

    def is_machine(self, user):
        return isinstance(user, MachineUser)


class IsMachineUserOrReadOnly(IsMachineUser):
    """
    Allow a machine user to access this resource, human readers can access the
    list and detail views.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return super(IsMachineUserOrReadOnly, self).has_permission(request, view)


class IsActiveMachineUser(IsMachineUser):
    """
    Allows only active replica objects to access this resource.
    """

    message = "only active replica clients have access permission to this resource"

    def has_permission(self, request, view):
        if super(IsActiveMachineUser, self).has_permission(request, view):
            return request.user.replica.active
        return False


class IsActiveMachineUserOrReadOnly(IsActiveMachineUser):
    """
    Allow an active machine user to access this resource, human readers can
    access the list and detail views.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return super(IsActiveMachineUserOrReadOnly, self).has_permission(request, view)
