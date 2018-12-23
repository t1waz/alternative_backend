from django.db import models


class BoardCompany(models.Model):
	description = models.CharField(max_length=500)
	company_name = models.CharField(max_length=200)

	def __str__(self):
		return '%s %s' % (self.id, self.company_name)

	class Meta:
		db_table = 'board_company'


class BoardModel(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=500)
	year = models.IntegerField()
	code = models.IntegerField()
	company = models.ForeignKey('BoardCompany',
								on_delete=models.CASCADE )

	def __str__(self):
		return '%s %s %s' % (self.code, self.company, self.year)

	class Meta:
		db_table = 'board_model'


class Board(models.Model):
	model = models.ForeignKey('BoardModel',
							on_delete=models.CASCADE)
	barcode = models.IntegerField(primary_key=True)
	company = models.ForeignKey('BoardCompany',
							on_delete=models.CASCADE )

	def __str__(self):
		return '%s' % (self.barcode)

	class Meta:
		db_table = 'board'


class BoardScan(models.Model):
	barcode_scan = models.ForeignKey('Board',
							on_delete=models.CASCADE)
	worker = models.ForeignKey('workers.Worker',
							on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	station = models.ForeignKey('stations.Station',
							on_delete=models.CASCADE )

	def __str__(self):
		return '%s %s %s' % (self.barcode_scan, self.worker, self.timestamp)

	class Meta:
		db_table = 'board_scan'
