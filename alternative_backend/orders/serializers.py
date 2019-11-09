from rest_framework import serializers
from orders.services import OrderService
from orders.validators import (
    SendedBoardValidation,
    DeleteSendedValidation,
    OrderValidation,
)
from boards.models import (
    Board,
    BoardModel,
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


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRecord
        fields = ('board_model', 'quantity')

    board_model = serializers.SlugRelatedField(many=False,
                                           queryset=BoardModel.objects.all(),
                                           slug_field='name')


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
        fields = ('id', 'client', 'timestamp', 'completed', 'records', 'sended')
        validators = [OrderValidation()]

    sended = serializers.SerializerMethodField('sended_boards')
    records = RecordSerializer(many=True,
                               read_only=False)
    client = serializers.SlugRelatedField(many=False,
                                          queryset=Client.objects.all(),
                                          slug_field='name')

    def sended_boards(self, obj):
        return [sended.board.barcode for sended in
                OrderService().get_sended_boards(order_id=obj.id)]

    def create(self, validated_data):
        order_records = validated_data.pop('records')
        order = Order.objects.create(**validated_data)

        OrderService().update_order_records(order=order,
                                            order_records=order_records)

        return order

    def update(self, instance, validated_data):
        records_to_update = validated_data.pop('records', None)

        if records_to_update:
            OrderService().update_order_records(order=instance,
                                                order_records=records_to_update)

        return super().update(instance, validated_data)
