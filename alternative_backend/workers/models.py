from django.db import models


class Worker(models.Model):
    username = models.CharField(max_length=30,
                                unique=True)
    barcode = models.IntegerField(primary_key=True,
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
        return '{} {}'.format(self.username, self.barcode)

    class Meta:
        db_table = 'workers'


class WorkerScan(models.Model):
    worker_barcode = models.ForeignKey('Worker',
                                       on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    started = models.BooleanField()
    year = models.IntegerField()
    month = models.IntegerField()
    week = models.IntegerField()
    day_name = models.CharField(max_length=80)
    seconds = models.BigIntegerField()

    def __str__(self):
        return '{}: {}'.format(self.worker_barcode, self.timestamp)

    class Meta:
        db_table = 'worker_scan'
