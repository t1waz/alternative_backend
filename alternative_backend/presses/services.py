from django.db import transaction
from events.services import EventService
from common.exceptions import ServiceException
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

    def start_mold_history_record(self, press, mold, event=None, **kwargs):
        if not event:
            event = EventService().create_event(worker=kwargs.get('worker'),
                                                operation_name='changing mold')
        try:
            MoldHistory.objects.create(press=press,
                                       mold=mold,
                                       started=event)
        except:  # TODO
            raise ServiceException('internal error - cannot create started mold record')

    def get_open_mold_history_records(self, press):
        try:
            return MoldHistory.objects.get(press=press,
                                           finished__isnull=True,
                                           started__isnull=False)
        except MoldHistory.DoesNotExist:
            return None
        except:  # TODO
            raise ServiceException('internal error - cannot find previous history mold record')

    @transaction.atomic
    def handle_history(self, worker, press, mold):
        open_record = self.get_open_mold_history_records(press=press)

        if getattr(open_record, 'mold', None) != mold.name:
            event = EventService().create_event(worker=worker,
                                                operation_name='changing mold')
            self.start_mold_history_record(press=press,
                                           mold=mold,
                                           event=event)
            if open_record:
                open_record.finished = event
                open_record.save()
