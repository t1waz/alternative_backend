from django.contrib import admin
from .models import (
    Press,
    MoldHistory,
)


admin.site.register(Press)
admin.site.register(MoldHistory)
