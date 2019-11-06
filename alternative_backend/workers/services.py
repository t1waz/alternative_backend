import common.auth as auth
from django.db import transaction
from events.services import EventService
from common.exceptions import ServiceException
from common.common import seconds_between_timestamps
from workers.models import (
    Worker,
    WorkerWorkHistory,
)


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

    def start_worker_history_record(self, worker, event=None):
        if not event:
            event = EventService().create_event(worker=worker,
                                                operation_name='work start')
        # try:
        return WorkerWorkHistory.objects.create(worker=worker,
                                                started=event)
        # except:  # TODO
        #     raise ServiceException('internal error - cannot create started mold record')

    def get_open_worker_history_record(self):
        try:
            return WorkerWorkHistory.objects.select_related('started').get(finished__isnull=True,
                                                                           started__isnull=False)
        except WorkerWorkHistory.DoesNotExist:
            return None
        except:  # TODO
            raise ServiceException('internal error - cannot find previous worker work record')

    @transaction.atomic
    def handle_worker_work_history(self, worker):
        open_record = self.get_open_worker_history_record()

        if open_record:
            event = EventService().create_event(worker=worker,
                                                operation_name='work finish')

            open_record.finished = event
            work_time = seconds_between_timestamps(start_timestamp=open_record.started.timestamp,
                                                   finish_timestamp=event.timestamp)
            open_record.work_time = work_time
            open_record.save()

        new_record = self.start_worker_history_record(worker=worker)

        return new_record
