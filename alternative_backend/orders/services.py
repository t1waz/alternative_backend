from django.db.models import Sum
from django.db import transaction
from stations.models import Station
from common.exceptions import ServiceException
from boards.models import (
    BoardModel,
    BoardCompany,
    BoardScan,
    Board,
)
from .models import (
    OrderRecord, 
    Order, 
    SendedBoard,
)


class OrderService:

    @transaction.atomic
    def update_order_records(self, order_id, order_records):
        order = Order.objects.get(id=order_id)
        OrderRecord.objects.filter(order=order).delete()
        records = []
        for board, quantity in order_records.items():
            record = OrderRecord(order=order,
                                 board_model=BoardModel.objects.get(name=board),
                                 quantity=quantity)
            records.append(record)

        try:
            OrderRecord.objects.bulk_create(records)
        except:    # TODO
            raise ServiceException('cannot update')

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
        companies_list = list()
        for company in BoardCompany.objects.all():
            orders = self.return_order_info(company_code=company.code)
            companies_list.append({company.name: orders})

        return companies_list

    def is_production_finish_for_board(self, barcode):
        last_station_id = list(Station.objects.all().values_list('id', flat=True))[-1]

        return BoardScan.objects.filter(barcode__barcode=barcode,
                                        station__id=last_station_id).exists()

    def board_exist(self, barcode):
        try:
            return Board.objects.filter(barcode=barcode).exists()
        except:    # TODO
            raise ServiceException('cannot check')

    def is_board_already_sended(self, board):
        try:
            return SendedBoard.objects.filter(board=board).exists()
        except:  # TODO
            raise ServiceException('incorrect data')

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
