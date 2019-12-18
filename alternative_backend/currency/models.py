from django.db import models
from currency.constans import SYMBOLS


class Currency(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=500,
                              choices=SYMBOLS)
    price = models.FloatField(null=True,
                              blank=True)

    def __str__(self):
        return f'{self.name} {self.symbol}'

