from django.contrib import admin
from .models import (
	Operation,
	Event
)


admin.site.register(Operation)
admin.site.register(Event)
