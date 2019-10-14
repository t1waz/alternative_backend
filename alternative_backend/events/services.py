from common.exceptions import ServiceException
from events.models import (
	Event,
	Operation,
)


class EventService:
	def create_event(self, worker, operation_name):
		operation, created = Operation.objects.get_or_create(name=operation_name)

		if not worker:
			raise ServiceException("create event worker data is incorrect")

		try:
			return Event.objects.create(person=worker,
										operation=operation)
		except:  # TODO
			ServiceException("cannot create new event")

	def create_operation(self, name):
		try:
			new_operation = Operation.objects.create(name=name)
		except:  # TODO
			new_operation = None

		return new_operation

	def get_operation(self, name):
		try:
			return Operation.objects.get(name=name)
		except Operation.DoesNotExist:
			return None
