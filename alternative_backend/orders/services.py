from django.db.models import Sum
from boards.models import (
    BoardModel,
    BoardCompany
)
from .models import OrderRecord, Order, SendedBoard


class OrderService:
    def update_order_records(self, order_id, order_records):
        order = Order.objects.get(id=order_id)

        for order_record in order_records:
            board_name = list(order_record.keys())[0]
            board = BoardModel.objects.get(name=board_name)
            qty = order_record[board_name]
            OrderRecord.objects.create(order=order,
                                       board_model=board,
                                       quantity=qty)

    def return_order_info(self, company_code):
        models = [model.name for model in
                  BoardModel.objects.filter(company__code=company_code)]
        order_dict = dict.fromkeys(models, 0)

        for model in models:
            order = OrderRecord.objects.filter(board_model__name=model,
                                               board_model__company__code=company_code).aggregate(
                Sum('quantity'))['quantity__sum'] or 0

            sended = SendedBoard.objects.filter(board__model__name=model,
                                                board__company__code=company_code).count() or 0

            order_dict[model] = order - sended
        return order_dict

    def return_order_info_for_all_companies(self):
        companies = BoardCompany.objects.all()
        companies_list = list()
        for company in companies:
            orders = self.return_order_info(company_code=company.code)
            if not orders[list(orders.keys())[0]] == {}:
                companies_list.append(orders)
        return companies_list
