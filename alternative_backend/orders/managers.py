from django.db import models


class ActiveOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(completed=False)