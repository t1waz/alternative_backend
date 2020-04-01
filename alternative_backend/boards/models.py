from django.db import models


class BoardCompany(models.Model):
    description = models.CharField(max_length=200)
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=200,
                            unique=True)

    def __str__(self):
        return f'{self.id} {self.name}'


class BoardGraphic(models.Model):
    description = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    year = models.IntegerField()
    name = models.CharField(max_length=200,
                        unique=True)

    def __str__(self):
        return f'{self.name} {self.year}'


class Layout(models.Model):
    top_graphic = models.ForeignKey('boards.BoardGraphic',
                                    on_delete=models.CASCADE,
                                    related_name='default_top_graphics',
                                    null=True,
                                    blank=True)
    bottom_graphic = models.ForeignKey('boards.BoardGraphic',
                                       on_delete=models.CASCADE,
                                       related_name='default_bottom_graphics',
                                       null=True,
                                       blank=True)
    top_material = models.ForeignKey('materials.Material',
                                     on_delete=models.CASCADE,
                                     related_name='default_top_materials',
                                     null=True,
                                     blank=True)
    bottom_material = models.ForeignKey('materials.Material',
                                        on_delete=models.CASCADE,
                                        related_name='default_bottom_materials',
                                        null=True,
                                        blank=True)

    def __str__(self):
        return f'{self.id}'


class BoardModel(models.Model):
    description = models.CharField(max_length=200)
    year = models.IntegerField()
    code = models.IntegerField(unique=True)
    layout_material_quantity = models.FloatField()
    name = models.CharField(max_length=50,
                            unique=True)
    materials = models.ManyToManyField('materials.Material',
                                       through='boards.boardmodelmaterial',
                                       verbose_name='model_materials')
    company = models.ForeignKey('boards.BoardCompany',
                                on_delete=models.CASCADE)
    layout = models.ForeignKey('boards.Layout',
                               on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.code} {self.company} {self.year} {self.name}'


class Board(models.Model):
    barcode = models.BigIntegerField(unique=True)
    second_category = models.BooleanField(default=False)
    press_time = models.IntegerField(default=0)
    model = models.ForeignKey('boards.BoardModel',
                              on_delete=models.CASCADE)
    company = models.ForeignKey('boards.BoardCompany',
                                on_delete=models.CASCADE)
    layout = models.ForeignKey('boards.Layout',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)

    def __str__(self):
        return f'{self.barcode}'


class BoardScan(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    barcode = models.ForeignKey('boards.Board',
                                on_delete=models.CASCADE)
    worker = models.ForeignKey('workers.Worker',
                               on_delete=models.CASCADE)
    station = models.ForeignKey('stations.Station',
                                on_delete=models.CASCADE)
    comment = models.CharField(max_length=100,
                               blank=True)

    def __str__(self):
        return f'{self.barcode} {self.worker} {self.timestamp}'


class BoardModelMaterial(models.Model):
    quantity = models.FloatField()
    model = models.ForeignKey('boards.BoardModel',
                              on_delete=models.CASCADE,
                              related_name='components')
    material = models.ForeignKey('materials.Material',
                                 on_delete=models.CASCADE)    

    class Meta:
        unique_together = ('material', 'model')

    def __str__(self):
        return f'{self.material.name} {self.model.name}'
