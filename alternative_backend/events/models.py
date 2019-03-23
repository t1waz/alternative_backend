from django.db import models


class Event(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	person = models.ForeignKey('workers.Worker',
                               on_delete=models.CASCADE)
