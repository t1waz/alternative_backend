from rest_framework import serializers
from .services import OrderService


class BoardsField(serializers.Field):
    def to_representation(self, value):
        return OrderService().get_order_records(order_id=value.id)

    def to_internal_value(self, data):
        self.context['boards'] = data

        return ''



class SendedField(serializers.Field):
    def to_representation(self, value):
        return [sended.board.barcode for sended in 
                OrderService().get_sended_boards(order_id=value.id)]

    def to_internal_value(self, data):
        return ''
