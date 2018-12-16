from django.db import models


class Worker(models.Model):
	name = models.CharField(max_length=30)
	surname = models.CharField(max_length=30)
	barcode = models.IntegerField()

	def __str__(self):
		return '%s %s' % (self.name, self.surname)

	class Meta:
		db_table = 'workers'