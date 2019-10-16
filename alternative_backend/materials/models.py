from django.db import models
from materials.constants import UNITS


class MaterialCategory(models.Model):
    description = models.CharField(max_length=500)
    name = models.CharField(max_length=500,
                            unique=True)

    def __str__(self):
        return "{} {}".format(self.id, self.name)


class Material(models.Model):
    description = models.CharField(max_length=500)
    price = models.FloatField()
    name = models.CharField(max_length=500,
                            unique=True)
    unit = models.CharField(max_length=500,
                            choices=UNITS)
    category = models.ForeignKey('MaterialCategory',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.category, self.name)


class MaterialPriceHistory(models.Model):
    price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    material = models.ForeignKey('Material',
                                 on_delete=models.CASCADE,
                                 related_name='history_material')
