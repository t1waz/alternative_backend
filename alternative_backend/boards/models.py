from django.db import models


class BoardCompany(models.Model):
    description = models.CharField(max_length=200)
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=200,
                            unique=True)

    def __str__(self):
        return "{} {}".format(self.id, self.name)

    class Meta:
        db_table = "board_company"


class BoardModel(models.Model):
    description = models.CharField(max_length=200)
    year = models.IntegerField()
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=50,
                            unique=True)
    materials = models.ManyToManyField('materials.material',
                                       through='boards.boardmodelmaterial',
                                       verbose_name='model_materials')
    company = models.ForeignKey('boards.boardcompany',
                                on_delete=models.CASCADE)

    def __str__(self):
        return "{} {} {} {}".format(self.code, self.company, self.year, self.name)

    class Meta:
        db_table = "board_model"


class Board(models.Model):
    barcode = models.BigIntegerField(unique=True)
    second_category = models.BooleanField(default=False)
    press_time = models.IntegerField(default=0)
    model = models.ForeignKey('boards.boardmodel',
                              on_delete=models.CASCADE)
    company = models.ForeignKey('boards.boardcompany',
                                on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.barcode)

    class Meta:
        db_table = "board"


class BoardScan(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    barcode = models.ForeignKey('boards.board',
                                on_delete=models.CASCADE)
    worker = models.ForeignKey('workers.Worker',
                               on_delete=models.CASCADE)
    station = models.ForeignKey('stations.Station',
                                on_delete=models.CASCADE)
    comment = models.CharField(max_length=100,
                               blank=True)

    def __str__(self):
        return "{} {} {}".format(self.barcode, self.worker, self.timestamp)

    class Meta:
        db_table = "board_scan"


class BoardModelMaterial(models.Model):
    quantity = models.FloatField()
    model = models.ForeignKey('boards.boardmodel',
                              on_delete=models.CASCADE,
                              related_name='components')
    material = models.ForeignKey('materials.material',
                                 on_delete=models.CASCADE)    

    def __str__(self):
        return "{} {}".format(self.material.name, self.model.name)
