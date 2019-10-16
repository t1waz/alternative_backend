from django.db import models


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
                                 related_name='history_finished',
                                 null=True,
                                 blank=True)

    def __str__(self):
        return "{} {}".format(self.press, self.mold)

    class Meta:
        db_table = "mold_history"


class Press(models.Model):
    press_time = models.IntegerField()
    name = models.CharField(max_length=200,
                            unique=True)

    @property
    def mold(self):
        current_mold_hisotry = MoldHistory.objects.get(press=self,
                                                       finished__isnull=True)

        return current_mold_hisotry.mold.name

    def __str__(self):
        return "{} {}".format(self.name, self.press_time)

    class Meta:
        db_table = "press"
