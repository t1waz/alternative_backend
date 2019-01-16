from rest_framework import serializers
from .models import Client, Order, OrderRecord, SendedBoard
from .services import order_service




class ClientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Client
		fields = ('id', 'name', 'country', 'city', 'post_code', 'adress', 'is_company')


class OrderRecordSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderRecord
		fields = ('id', 'order', 'board_model', 'quantity', 'order_position')


class SendedBoardSerializer(serializers.ModelSerializer):
	def validate_if_can_be_added(self, board):
		#tutaj zajebac kod

	class Meta:
		model = SendedBoard
		fields = ('id', 'board', 'order', 'timestamp')


class OrderSerializer(serializers.ModelSerializer):
	client = serializers.SlugRelatedField(many=False,
										  queryset=Client.objects.all(),
										  slug_field='name')
	boards = serializers.SlugRelatedField(many=True,
										  read_only=True,
										  slug_field='order_position')
	sended = serializers.SerializerMethodField('sended_boards')

	def sended_boards(self,obj):
		sended_boards = SendedBoard.objects.filter(
			order=obj.id).values_list('board__barcode', flat=True)
		return sended_boards

	def create(self, validated_data):
		order = Order.objects.create(**validated_data)
		order_service.update_order_records(order_id=order.id, 
										   order_records=self.context['boards'])

		return order

	def update(self, instance, validated_data):
		if self.context['boards']:
			OrderRecord.objects.filter(order=instance.pk).delete()
			order_service.update_order_records(order_id=instance.pk,
											   order_records=self.context['boards'])

		return super().update(instance, validated_data)

	class Meta:
		model = Order
		fields = ('id', 'client', 'timestamp', 'completed', 'boards', 'sended') 
