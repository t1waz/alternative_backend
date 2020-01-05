import uuid
import redis
from time import time
from django.conf import settings
from workers.services import WorkerService
from cryptography.fernet import Fernet, InvalidToken


class RedisMemoryService:
    def __init__(self):
        self.redis_db = redis.Redis(host=settings.REDIS_HOST_NAME,
                                    port=settings.REDIS_PORT,
                                    db=settings.REDIS_DB_NUMBER)

    def set_value(self, key, value):
        self.redis_db.set(key, value)

    def get_value(self, key):
        data = self.redis_db.get(key) or ''
        if data:
            data = data.decode()

        return data


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

        return token.split(':')[0]

    def get_encrypted_data(self, data):
        return self.crypto_worker.encrypt(data.encode()).decode()

    def generate_new_token(self, username):
        user_flag = uuid.uuid4().hex
        current_flags = RedisMemoryService().get_value(key=username) or user_flag

        if len(current_flags.split(':')) >= settings.MAX_NUMBER_OF_TOKENS:
            return None
        else:
            current_flags = f'{current_flags}:{user_flag}'

        RedisMemoryService().set_value(key=username,
                                       value=current_flags.encode())

        return self.get_encrypted_data(f'{username}:{user_flag}')

    def validate_token(self, token):
        decrypted_token = self.decrypt_token(token)

        if not decrypted_token:
            return False

        current_seconds = int(time())
        last_seconds = self.crypto_worker.extract_timestamp(token.encode())

        if current_seconds - last_seconds > settings.TOKEN_VALID_TIME:
            return False

        username, flag = decrypted_token.split(':')
        flags = RedisMemoryService().get_value(username).split(':')
        if flag in flags:
            return True

        return False
