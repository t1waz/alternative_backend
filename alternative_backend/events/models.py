from django.db import models


class Operation(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Event(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey('workers.Worker',
                               on_delete=models.CASCADE)
    operation = models.ForeignKey('Operation',
                                  on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.person.name} {self.operation.name} {self.timestamp}'
