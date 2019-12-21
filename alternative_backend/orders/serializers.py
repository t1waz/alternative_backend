from rest_framework import serializers
from orders.services import OrderService
from boards.serializers import BoardModelLayoutSerializer
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


class RecordSerializer(serializers.ModelSerializer):
    layout = BoardModelLayoutSerializer(many=False,
                                        required=False,
                                        allow_null=True)
    board_model = serializers.SlugRelatedField(many=False,
                                           queryset=BoardModel.objects.all(),
                                           slug_field='name')

    class Meta:
        model = OrderRecord
        fields = ('board_model', 'quantity', 'layout')


class SendedBoardSerializer(serializers.ModelSerializer):
    board = serializers.SlugRelatedField(many=False,
                                         queryset=Board.objects.all(),
                                         slug_field='barcode')

    class Meta:
        model = SendedBoard
        fields = ('id', 'board', 'order')
        validators = [SendedBoardValidation()]


class DeleteSendedSerializer(SendedBoardSerializer):
    class Meta:
        model = SendedBoard
        fields = ('id', 'board', 'order')
        validators = [DeleteSendedValidation()]


class OrderSerializer(serializers.ModelSerializer):
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
        return OrderService().create_order(validated_data)

    def update(self, instance, validated_data):
        return OrderService().update_order(instance=instance,
                                           validated_data=validated_data)

    class Meta:
        model = Order
        fields = ('id', 'client', 'timestamp', 'completed', 'records', 'sended')
        validators = [OrderValidation()]
