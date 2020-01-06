from django.db.models import Sum
from django.db import transaction
from stations.models import Station
from boards.services import BoardService
from common.exceptions import ServiceException
from boards.models import (
    Board,
    BoardScan,
    BoardModel,
    BoardCompany,
)
from orders.models import (
    Order,
    OrderRecord,
    SendedBoard,
)


class OrderService:
    def create_records(self, order, data):
        records = []
        for record in data:
            layout = None
            if 'layout' in record:
                layout = BoardService().get_layout(**record['layout'])

            records.append(OrderRecord(order=order,
                                       board_model=record.get('board_model'),
                                       quantity=record.get('quantity'),
                                       layout=layout))

        try:
            OrderRecord.objects.bulk_create(records)
        except:    # TODO
            raise ServiceException('cannot create order records')

    @transaction.atomic
    def create_order(self, validated_data):
        order_records_data = validated_data.pop('records', [])

        try:
            order = Order.objects.create(**validated_data)
        except:    # TODO
            raise ServiceException('cannot create order')

        self.create_records(order=order,
                            data=order_records_data)

        return order

    @transaction.atomic
    def update_order(self, instance, validated_data):
        order_records_data = validated_data.pop('records', [])
        if order_records_data:
            instance.records.all().delete()
            self.create_records(order=instance,
                                data=order_records_data)

        try:
            for attribute, value in validated_data.items():
                setattr(instance, attribute, value)
            instance.save()
        except:    # TODO
            raise ServiceException('cannot update order record - invalid order data')

        return instance

    def return_order_info(self, company_code):
        order_dict = dict()
        for model in [model.name for model in 
                      BoardModel.objects.filter(company__code=company_code)]:
            order = OrderRecord.objects.filter(board_model__name=model,
                                               board_model__company__code=company_code).aggregate(
                                               Sum('quantity'))['quantity__sum'] or 0
            sended = SendedBoard.objects.filter(board__model__name=model,
                                                board__company__code=company_code).count() or 0
            order_dict[model] = order - sended

        return order_dict

    def return_order_info_for_all_companies(self):
        return [{name: self.return_order_info(company_code=code)} for name, code in
                BoardCompany.objects.all().values_list('name', 'code')]

    def is_production_finish_for_board(self, barcode):
        last_station_id = Station.objects.all().values_list(
            'id', flat=True).order_by('production_step').last()

        return BoardScan.objects.filter(barcode__barcode=barcode,
                                        station__id=last_station_id).exists()

    def board_exist(self, barcode):
        return Board.objects.filter(barcode=barcode).exists()

    def is_board_already_sended(self, board):
        return SendedBoard.objects.filter(board=board).exists()

    def get_order_quantity(self, board, order_id):
        try:
            order_qty = sum(OrderRecord.objects.filter(order=order_id,
                                                       board_model=board.model).values_list(
                                                       'quantity', flat=True))

            return order_qty
        except:  # TODO
            raise ServiceException('incorrect data')

    def valid_order_quantity(self, board, order_id):
        order_qty = sum(OrderRecord.objects.filter(order=order_id,
                                                   board_model=board.model).values_list(
                                                   'quantity', flat=True))
        sended_qty = SendedBoard.objects.filter(order=order_id,
                                                board__model=board.model).count()

        return sended_qty <= order_qty and order_qty

    def get_order_records(self, order_id):
        return {order.board_model.name: order.quantity for order in 
                OrderRecord.objects.filter(order=order_id)}

    def get_sended_boards(self, order_id):
        return SendedBoard.objects.filter(order=order_id).select_related('board')
