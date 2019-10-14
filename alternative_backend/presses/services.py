from events.services import EventService
from common.exceptions import ServiceException
from django.db import transaction
from presses.models import (
    Press,
    MoldHistory,
)


class PressService:
    def get_press_from_name(self, name):
        try:
            return Press.objects.get(name=name)
        except Press.DoesNotExist:
            return None
        except:
            raise ServiceException('incorrect input data')

    def get_open_mold_history_records(self, press):
        try:
            return MoldHistory.objects.get(press=press,
                                           finished__isnull=True)
        except MoldHistory.DoesNotExist:
            raise ServiceException('internal error - cannot find previous history mold record')

    @transaction.atomic
    def handle_history(self, worker, press, mold):
        status = False
        open_record = self.get_open_mold_history_records(press=press)

        if open_record.mold.name != mold.name:
            event = EventService().create_event(worker=worker,
                                                operation_name='changing mold')
            open_record.finished = event
            open_record.save()

            MoldHistory.objects.create(press=press,
                                       mold=mold,
                                       started=event)
            status = True

        return status
