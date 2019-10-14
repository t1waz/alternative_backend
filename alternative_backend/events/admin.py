from django.contrib import admin
from events.models import (
	Operation,
	Event
)


admin.site.register(Operation)
admin.site.register(Event)
