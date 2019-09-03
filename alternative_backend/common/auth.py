from django.conf import settings
from rest_framework import permissions


class BaseAccess(permissions.BasePermission):
    """
    Checks if request got valid access key
    """
    def has_permission(self, request, view):
        request_token = request.META.get('HTTP_ACCESS_TOKEN', None)
        return request_token == settings.ACCESS_KEY
