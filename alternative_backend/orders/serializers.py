from rest_framework import serializers
from orders.services import OrderService
from orders.fields import (
    BoardsField,
    SendedField,
)
from orders.validators import (
    SendedBoardValidation,
    DeleteSendedValidation,
    OrderValidation,
)
from boards.models import (
    Board,
)
from orders.models import (
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
        validators = [SendedBoardValidation()]

    board = serializers.SlugRelatedField(many=False,
                                         queryset=Board.objects.all(),
                                         slug_field='barcode')


class DeleteSendedSerializer(SendedBoardSerializer):
    class Meta:
        model = SendedBoard
        fields = ('id', 'board', 'order')
        validators = [DeleteSendedValidation()]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'client', 'timestamp', 'completed', 'boards', 'sended')
        validators = [OrderValidation()]

    sended = serializers.SerializerMethodField('sended_boards')
    boards = BoardsField(source='*')
    sended = SendedField(source='*', read_only=True)
    client = serializers.SlugRelatedField(many=False,
                                          queryset=Client.objects.all(),
                                          slug_field='name')

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        OrderService().update_order_records(order_id=order.id,
                                            order_records=self.context['boards'])

        return order

    def update(self, instance, validated_data):
        boards_to_update = self.context.get('boards')

        if boards_to_update:
            OrderService().update_order_records(order_id=instance.pk,
                                                order_records=boards_to_update)

        return super().update(instance, validated_data)
