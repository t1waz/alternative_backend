from django.db import models


class MoldHistory(models.Model):
    press = models.ForeignKey('Press',
                              on_delete=models.CASCADE,
                              related_name='history_press')
    mold = models.ForeignKey('boards.BoardModel',
                             on_delete=models.CASCADE,
                             related_name='history_mold',
                             blank=True,
                             null=True)
    started = models.ForeignKey('events.Event',
                                on_delete=models.CASCADE,
                                related_name='history_mold_started')
    finished = models.ForeignKey('events.Event',
                                 on_delete=models.CASCADE,
                                 related_name='history_mold_finished',
                                 null=True,
                                 blank=True)

    def __str__(self):
        return f'{self.press.name} {self.mold.name}'


class Press(models.Model):
    press_time = models.IntegerField()
    mold = models.ForeignKey('boards.BoardModel',
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True)
    name = models.CharField(max_length=200,
                            unique=True)

    def __str__(self):
        return f'{self.name} {self.press_time}'
