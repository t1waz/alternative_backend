from django.db import models


class Operation(models.Model):
    name = models.CharField(max_length=500)


class Event(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey('workers.Worker',
                               on_delete=models.CASCADE)
    operation = models.ForeignKey('Operation',
                                  on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.person, self.operation.name)

    class Meta:
        db_table = "event"
