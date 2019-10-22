from time import time
from django.conf import settings
from rest_framework import permissions
from workers.services import WorkerService
from cryptography.fernet import Fernet, InvalidToken


class TokenService:
    def __init__(self):
        self.crypto_worker = Fernet(settings.CRYPTO_KEY)

    def generate_secret_key(self):
        return Fernet.generate_key()

    def decrypt_token(self, token):
        try:
            return self.crypto_worker.decrypt(token.encode()).decode()
        except (InvalidToken, ValueError, AttributeError):
            return None

    def get_worker_username(self, token):
        return token[10:]

    def generate_new_token(self, worker_name):
        current_seconds = str(int(time())).encode()
        worker = worker_name.encode()

        return self.crypto_worker.encrypt(current_seconds + worker).decode()

    def validate_token(self, token):
        decrypted_token = self.decrypt_token(token)

        if not decrypted_token:
            return False

        current_seconds = int(time())
        last_seconds = int(decrypted_token[:10])
        if current_seconds - last_seconds > settings.TOKEN_VALID_TIME:
            return False

        if WorkerService().is_worker_for_username(username=decrypted_token[10:]):
            return True

        return False


class BaseAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        request_token = request.META.get('HTTP_ACCESS_TOKEN')

        if not request_token:
            return False

        if TokenService().validate_token(token=request_token):
            return True

        return False
