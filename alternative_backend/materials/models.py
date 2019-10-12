from django.db import models
from model_utils import FieldTracker
from materials.constants import UNITS


class MaterialCategory(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500)

    def __str__(self):
        return "{} {}".format(self.id, self.name)


class Material(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    price = models.FloatField()
    tracker = FieldTracker(fields=['price'])
    unit = models.CharField(max_length=500,
                            choices=UNITS)
    category = models.ForeignKey('MaterialCategory',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.category, self.name)


class MaterialPriceHistory(models.Model):
    price = models.FloatField()
    material = models.ForeignKey('Material',
                                 on_delete=models.CASCADE,
                                 related_name='history_material')
    established = models.ForeignKey('events.event',
                                    on_delete=models.CASCADE,
                                    related_name='history_established')


class BoardModelComponent(models.Model):
    quantity = models.FloatField()
    model = models.ForeignKey('boards.boardmodel',
                              on_delete=models.CASCADE)
    material = models.ForeignKey('Material',
                                 on_delete=models.CASCADE)
