from rest_framework import serializers
from .services import OrderService
from alternative_backend.exceptions import AppException
from boards.models import (
    Board,
    BoardModel
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
        try:
            board_model = BoardModel.objects.get(code=int(str(self.initial_data['board'])[2:4]))
            order_qty = OrderRecord.objects.get(order=self.initial_data['order'],
                                                board_model=board_model).quantity
        except:
            raise AppException("CANNOT ADD")
        sended_qty = SendedBoard.objects.filter(order=self.initial_data['order'],
                                                board__model=board_model).count()
        ifsend = SendedBoard.objects.filter(board__barcode=self.initial_data['board']).exists()
        if sended_qty >= order_qty:
            raise AppException("FULL")
        if ifsend:
            raise AppException("ALREADY SENDED")

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
        if len(self.context['boards']) == 0:
            raise AppException('no boards in order')

        return data

    def order_boards(self, obj):
        ordered_boards = {}
        orders = OrderRecord.objects.filter(order=obj.id)
        for order in orders:
            ordered_boards[order.board_model.name] = order.quantity
        return ordered_boards

    def sended_boards(self, obj):
        sended_boards = SendedBoard.objects.filter(order=obj.id).values_list(
            'board__barcode', flat=True)
        return sended_boards

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