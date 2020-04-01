from django.contrib import admin

from workers.models import (
    Worker,
    WorkerWorkHistory,
)


admin.site.register(Worker)
admin.site.register(WorkerWorkHistory)
