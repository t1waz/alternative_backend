from django.contrib import admin
from workers.models import (
    Worker,
    WorkerScan
)


admin.site.register(Worker)
admin.site.register(WorkerScan)
