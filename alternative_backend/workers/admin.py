from django.contrib import admin
from .models import (
    Worker,
    WorkerScan
)


admin.site.register(Worker)
admin.site.register(WorkerScan)
