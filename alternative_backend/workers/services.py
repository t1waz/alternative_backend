from django.db import transaction

from common.exceptions import ServiceException
from common.helpers import seconds_between_timestamps
from events.services import EventService
from workers.models import (
    Worker,
    WorkerWorkHistory,
)


class WorkerService:
    def get_worker(self, username, password):
        return Worker.objects.filter(username=username,
                                     password=password).first()

    def get_worker_from_barcode(self, barcode):
        return Worker.objects.filter(barcode=barcode).first()

    def get_worker_from_username(self, username):
        return Worker.objects.filter(username=username).first()

    def start_worker_history_record(self, worker, event=None):
        if not event:
            event = EventService().create_event(worker=worker,
                                                operation_name='work start')
        try:
            return WorkerWorkHistory.objects.create(worker=worker,
                                                    started=event)
        except:  # TODO
            raise ServiceException('internal error - cannot create started mold record')

    def get_open_worker_history_record(self):
        return WorkerWorkHistory.objects.select_related(
                                    'started').filter(finished__isnull=True,
                                                      started__isnull=False).first()

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
