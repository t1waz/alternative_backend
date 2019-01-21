from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return "{} {}".format(self.id, self.name)

    class Meta:
        db_table = 'station'
