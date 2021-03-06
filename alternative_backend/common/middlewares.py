from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from alternative_backend.services import TokenService
from workers.services import WorkerService


class IdentityProviderMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.META.get('HTTP_COOKIE'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        token = request.META.get('HTTP_ACCESS_TOKEN')

        encrypted_token = TokenService().decrypt_token(token=token)

        if encrypted_token:
            username = TokenService().get_worker_username(token=encrypted_token)
            worker = WorkerService().get_worker_from_username(username=username)
            request.user = worker or AnonymousUser

        if not self.get_response:
            return request
