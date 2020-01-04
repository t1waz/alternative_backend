from rest_framework import permissions
from alternative_backend.services import TokenService


class BaseAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        request_token = request.META.get('HTTP_ACCESS_TOKEN')

        if not request_token:
            return False

        if TokenService().validate_token(token=request_token):
            return True

        return False
