from django.db.models import Sum
from stations.models import Station
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
    def update_order_records(self, order_id, order_records):
        for board in order_records.keys():
            OrderRecord.objects.create(order=Order.objects.get(id=order_id),
                                       board_model=BoardModel.objects.filter(name=board)[0],
                                       quantity=order_records[board])

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
        return Board.objects.filter(barcode=barcode).exists()

    def already_sended(self, barcode):
        return SendedBoard.objects.filter(board__barcode=barcode).exists()

    def valid_order(self, barcode, order_id):
        board_model = Board.objects.values_list('model', flat=True).get(barcode=barcode)
        order_qty = sum(OrderRecord.objects.filter(order=order_id,
                                                   board_model=board_model).values_list(
                                                   'quantity', flat=True))

        return order_qty      

    def valid_order_quantity(self, barcode, order_id):
        board_model = Board.objects.values_list('model', flat=True).get(barcode=barcode)
        order_qty = sum(OrderRecord.objects.filter(order=order_id,
                                                   board_model=board_model).values_list(
                                                   'quantity', flat=True))
        sended_qty = SendedBoard.objects.filter(order=order_id,
                                                board__model=board_model).count()

        return sended_qty <= order_qty and order_qty

    def remove_order_record(self, barcode, order_id):
        try:
            SendedBoard.objects.get(board__barcode=barcode,
                                    order=order_id)
            return True
        except:
            # handle this exception
            return False
