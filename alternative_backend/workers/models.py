from django.db import models


class Worker(models.Model):
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=30,
                                unique=True)
    barcode = models.BigIntegerField(primary_key=True,
                                     unique=True)

    @property
    def name(self):
        return self.username.split(' ')[0]

    @property
    def surname(self):
        try:
            surname = self.username.split(' ')[1]
        except IndexError:
            surname = ""
        return surname

    def __str__(self):
        return f'{self.username}'


class WorkerWorkHistory(models.Model):
    worker = models.ForeignKey('Worker',
                               on_delete=models.CASCADE)
    started = models.ForeignKey('events.Event',
                                on_delete=models.CASCADE,
                                related_name='history_work_started')
    finished = models.ForeignKey('events.Event',
                                 on_delete=models.CASCADE,
                                 related_name='history_work_finished',
                                 null=True,
                                 blank=True)
    work_time = models.BigIntegerField(null=True,
                                       blank=True)

    def __str__(self):
        return f'{self.worker}: {self.started.timestamp}'
