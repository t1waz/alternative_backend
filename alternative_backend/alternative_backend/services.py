from time import time
from django.conf import settings
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

    def get_worker_username(self, token, decrypted=True):
        if not decrypted:
            token = self.decrypt_token(token)

        if not token:
            return None

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

    def get_token_for_user(self, username, password):
        token = None
        worker = WorkerService().get_worker_from_username_and_password(username=username,
        															   password=password)
        if worker:
            token = self.generate_new_token(worker_name=username)

        return token
