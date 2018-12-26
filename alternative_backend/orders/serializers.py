from rest_framework import serializers
from .models import Client, Order, OrderRecord, SendedBoard


class ClientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Client
		fields = ('id', 'name', 'country', 'city', 'post_code', 'adress', 'is_company')


class OrderRecordSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderRecord
		fields = ('id', 'order', 'board_model', 'quantity')


class OrderRecords(serializers.RelatedField):
	def to_representation(self, value):
		board_name = value.board_model.name
		board_quantity = value.quantity
		boards = { board_name: board_quantity}
		return boards

	def to_internal_value(self, data):

		board_model = data.keys()
		print(board_model)
		client_name = self.context['request'].data['client']
		order = Order.objects.get(pk=1)
		return OrderRecord(order=order, board_model=board_model, quantity=data[board_model])

class OrderSerializer(serializers.ModelSerializer):
	client = serializers.SlugRelatedField(many=False,
										  queryset=Client.objects.all(),
										  slug_field='name')
	boards = OrderRecords(many=True,queryset=Order.objects.all())
	class Meta:
		model = Order
		fields = ('id', 'client', 'timestamp', 'completed', 'boards') 

class SendedBoardSerializer(serializers.ModelSerializer):
	class Meta:
		model = SendedBoard
		fields = ('id', 'order', 'timestamp')
