from django.db import models


class MoldHistory(models.Model):
    press = models.ForeignKey('Press',
                              on_delete=models.CASCADE,
                              related_name='history_press')
    mold = models.ForeignKey('boards.boardmodel',
                             on_delete=models.CASCADE,
                             related_name='history_mold',
                             blank=True,
                             null=True)
    started = models.ForeignKey('events.event',
                                on_delete=models.CASCADE,
                                related_name='history_mold_started')
    finished = models.ForeignKey('events.event',
                                 on_delete=models.CASCADE,
                                 related_name='history_mold_finished',
                                 null=True,
                                 blank=True)

    def __str__(self):
        return "{} {}".format(self.press, self.mold)

    class Meta:
        db_table = "mold_history"


class Press(models.Model):
    press_time = models.IntegerField()
    mold = models.ForeignKey('boards.boardmodel',
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True)
    name = models.CharField(max_length=200,
                            unique=True)

    def __str__(self):
        return "{} {}".format(self.name, self.press_time)

    class Meta:
        db_table = "press"
