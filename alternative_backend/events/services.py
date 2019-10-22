from common.exceptions import ServiceException
from workers.models import Worker
from events.models import (
    Event,
    Operation,
)


class EventService:
    def create_event(self, worker: Worker, operation_name: str) -> Event:
        operation, created = Operation.objects.get_or_create(name=operation_name)

        try:
            return Event.objects.create(person=worker,
                                        operation=operation)
        except:  # TODO
            ServiceException("cannot create new event")

    def create_operation(self, name: str) -> Operation:
        try:
            return Operation.objects.create(name=name)
        except:  # TODO
            ServiceException("cannot create operation")

    def get_operation(self, name: str) -> Operation:
        try:
            return Operation.objects.get(name=name)
        except Operation.DoesNotExist:
            return None
