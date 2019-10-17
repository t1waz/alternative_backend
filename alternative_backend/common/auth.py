from django.conf import settings
from rest_framework import permissions
from workers.services import WorkerService


class BaseAccess(permissions.BasePermission):
    """
    Checks if request got valid access key
    """
    def has_permission(self, request, view):
        valid_tokens = WorkerService().get_passwords()
        request_token = request.META.get('HTTP_ACCESS_TOKEN', None)
        valid_tokens.append(settings.ACCESS_KEY )

        return request_token in valid_tokens
