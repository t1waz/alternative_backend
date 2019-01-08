from django.db import models


class Client(models.Model):
	name = models.CharField(max_length=100)
	country = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	post_code = models.CharField(max_length=20)
	adress = models.CharField(max_length=100)
	is_company = models.BooleanField()

	def __str__(self):
		return '%s %s' % (self.name, self.country)

	class Meta:
		db_table = 'client'


class ActiveOrderManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(completed=False)


class Order(models.Model):
	client = models.ForeignKey('Client',
								on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	completed = models.BooleanField(default=False,
									blank=True)

	objects = models.Manager()
	active_orders = ActiveOrderManager()

	def __str__(self):
		return '%s %s' %(self.id, self.client)

	class Meta:
		db_table = 'order'


class SendedBoard(models.Model):
	board = models.ForeignKey('boards.board',
							  on_delete=models.CASCADE, related_name='send_boards')
	order = models.ForeignKey('Order',
							  on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return '%s %s' %(self.board, self.order)

	class Meta:
		db_table = 'sended_board'


class OrderRecord(models.Model):
	order = models.ForeignKey('Order',
							   on_delete=models.CASCADE,
							   related_name='boards')
	board_model = models.ForeignKey('boards.boardmodel',
									 on_delete=models.CASCADE)
	quantity = models.IntegerField()


	@property
	def order_position(self):
		position = {self.board_model.name: self.quantity}
		return position

	def __str__(self):
		return '%s %s %s' %(self. order, self.board_model, self.quantity)

	class Meta:
		db_table = 'order_record'