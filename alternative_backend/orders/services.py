from django.db.models import Sum
from boards.models import (
    BoardModel,
    BoardCompany
)
from .models import (
    OrderRecord, 
    Order, 
    SendedBoard
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
            if not orders[list(orders.keys())[0]] == {}:
                companies_list.append({company.name: orders})

        return companies_list
