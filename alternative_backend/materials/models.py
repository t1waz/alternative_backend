from django.db import models
from materials.constants import UNITS


class MaterialCategory(models.Model):
    description = models.CharField(max_length=500)
    name = models.CharField(max_length=500,
                            unique=True)

    def __str__(self):
        return f'{self.id} {self.name}'


class Material(models.Model):
    description = models.CharField(max_length=500)
    price = models.FloatField()
    currency = models.ForeignKey('currency.Currency',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=50,
                            unique=True)
    unit = models.CharField(max_length=50,
                            choices=UNITS)
    category = models.ForeignKey('MaterialCategory',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category} {self.name}'


class MaterialPriceHistory(models.Model):
    price = models.FloatField()
    currency = models.ForeignKey('currency.Currency',
                                 on_delete=models.CASCADE)
    started = models.ForeignKey('events.Event',
                                on_delete=models.CASCADE,
                                related_name='history_material_price_started')
    finished = models.ForeignKey('events.Event',
                                 on_delete=models.CASCADE,
                                 related_name='history_material_price_finished',
                                 null=True,
                                 blank=True)
    material = models.ForeignKey('Material',
                                 on_delete=models.CASCADE,
                                 related_name='history_material')

    def __str__(self):
        return f'{self.material.name} {self.price} {self.currency.symbol}'
