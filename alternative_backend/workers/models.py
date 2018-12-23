from django.db import models


class Worker(models.Model):
	username = models.CharField(max_length=30)
	barcode = models.IntegerField(primary_key=True)

	@property
	def name(self):
		return self.username.split(' ')[0]
	
	@property
	def surname(self):
		try:
			surname = self.username.split(' ')[1]
		except IndexError:
			surname = ""
		return surname
	
	def __str__(self):
		return '%s %s' % (self.username, self.barcode)

	class Meta:
		db_table = 'workers'