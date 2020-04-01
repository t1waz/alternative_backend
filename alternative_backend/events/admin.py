from django.contrib import admin

from events.models import (
	Event,
	Operation,
)


admin.site.register(Operation)
admin.site.register(Event)
