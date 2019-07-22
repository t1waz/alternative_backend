from rest_framework import serializers
from .services import OrderService
from alternative_backend.exceptions import AppException
from boards.models import (
    Board,
)
from .models import (
    Client,
    Order,
    OrderRecord,
    SendedBoard
)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'name', 'country', 'city', 'post_code', 'adress', 'is_company')


class OrderRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRecord
        fields = ('id', 'order', 'board_model', 'quantity', 'order_position')


class SendedBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendedBoard
        fields = ('id', 'board', 'order')

    board = serializers.SlugRelatedField(many=False,
                                         queryset=Board.objects.all(),
                                         slug_field='barcode')

    def is_valid(self, raise_exception=False):
        barcode = int(self.initial_data['board'])
        order_id = int(self.initial_data['order'])

        if not OrderService().board_exist(barcode=barcode):
            raise AppException("WRONG BARCODE")
        if OrderService().already_sended(barcode=barcode):
            raise AppException("ALREADY SENDED")
        if not OrderService().valid_order(barcode=barcode,
                                          order_id=order_id):
            raise AppException("WRONG ORDER")
        if not OrderService().valid_order_quantity(barcode=barcode,
                                                   order_id=order_id):
            raise AppException("ORDER FULL")

        return super().is_valid(raise_exception=False)


class DeleteSendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendedBoard
        fields = ('id', 'board', 'order')

    board = serializers.SlugRelatedField(many=False,
                                     queryset=Board.objects.all(),
                                     slug_field='barcode')

    def is_valid(self, raise_exception=False):
        barcode = int(self.initial_data['board'])
        order_id = int(self.initial_data['order'])

        if not OrderService().already_sended(barcode=barcode):
            raise AppException("WRONG BARCODE")

        if not OrderService().valid_order(barcode=barcode,
                                          order_id=order_id):
            raise AppException("WRONG ORDER")

        return super().is_valid(raise_exception=False)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'client', 'timestamp', 'completed', 'boards', 'sended')

    client = serializers.SlugRelatedField(many=False,
                                          queryset=Client.objects.all(),
                                          slug_field='name')
    sended = serializers.SerializerMethodField('sended_boards')
    boards = serializers.SerializerMethodField('order_boards')

    def validate(self, data):
        boards = self.context.get('boards', None)
        if self.context.get('request_method') == 'POST':
            if type(boards) is not dict:
                raise AppException('invalid boards')

        return data

    def order_boards(self, obj):
        ordered_boards = {}
        orders = OrderRecord.objects.filter(order=obj.id)
        for order in orders:
            ordered_boards[order.board_model.name] = order.quantity
        return ordered_boards

    def sended_boards(self, obj):
        sended_boards = list(SendedBoard.objects.filter(order=obj.id).values_list(
            'board__barcode', flat=True))

        if sended_boards: 
            return sended_boards 
        else: 
            return None

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        OrderService().update_order_records(order_id=order.id,
                                            order_records=self.context['boards'])

        return order

    def update(self, instance, validated_data):
        if self.context['boards']:
            OrderRecord.objects.filter(order=instance.pk).delete()
            OrderService().update_order_records(order_id=instance.pk,
                                                order_records=self.context['boards'])

        return super().update(instance, validated_data)
