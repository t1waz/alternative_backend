from django.db import models
from model_utils import FieldTracker


class Press(models.Model):
    name = models.CharField(max_length=200)
    mold = models.ForeignKey('boards.boardmodel',
                             on_delete=models.CASCADE,
                             related_name='actual_mold')
    tracker = FieldTracker(fields=['mold'])


class MoldHistory(models.Model):
    press = models.ForeignKey('Press',
                              on_delete=models.CASCADE,
                              related_name='history_press')
    mold = models.ForeignKey('boards.boardmodel',
                             on_delete=models.CASCADE,
                             related_name='history_mold')
    started = models.ForeignKey('events.event',
                                on_delete=models.CASCADE,
                                related_name='history_started')
    finished = models.ForeignKey('events.event',
                                 on_delete=models.CASCADE,
                                 related_name='history_finished')
