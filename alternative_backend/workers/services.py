import common.auth as auth
from django.db import transaction
from workers.models import Worker
from common.exceptions import ServiceException


class WorkerService:
    def is_worker_for_username(self, username):
        return Worker.objects.filter(username=username).exists()

    def get_worker_from_username_and_password(self, username, password):
        try:
            return Worker.objects.get(username=username,
                                      password=password)
        except Worker.DoesNotExist:
            return None
        except:
            raise ServiceException('cannot return token - internal error')

    def get_worker_from_barcode(self, barcode):
        try:
            return Worker.objects.get(barcode=barcode)
        except (Worker.DoesNotExist, ValueError):
            return None

    def get_worker_from_username(self, username):
        try:
            return Worker.objects.get(username=username)
        except (Worker.DoesNotExist, ValueError):
            return None

    @transaction.atomic
    def get_token(self, username, password):
        token = None
        worker = self.get_worker_from_username_and_password(username=username,
                                                            password=password)

        if worker:
            token = auth.TokenService().generate_new_token(worker_name=username)
            worker.token = token
            worker.save()

        return token
