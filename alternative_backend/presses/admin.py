from django.contrib import admin
from presses.models import (
    Press,
    MoldHistory,
)


admin.site.register(Press)
admin.site.register(MoldHistory)
