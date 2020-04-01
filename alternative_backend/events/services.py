from django.db import transaction

from common.exceptions import ServiceException
from events.models import (
    Event,
    Operation,
)
from workers.models import Worker


class EventService:
    @transaction.atomic
    def create_event(self, worker: Worker, operation_name: str) -> Event:
        try:
            operation, created = Operation.objects.get_or_create(name=operation_name)
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
