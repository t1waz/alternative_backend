from django.db import models


class Station(models.Model):
    description = models.CharField(max_length=200)
    production_step = models.IntegerField()
    name = models.CharField(max_length=50,
                            unique=True)

    def __str__(self):
        return f'{self.id} {self.name}'
