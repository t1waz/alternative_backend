import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ["SETTINGS_PATH"])

app = Celery('alternative_backend')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
