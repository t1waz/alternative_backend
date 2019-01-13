from .models import OrderRecord, Order, Client, SendedBoard
from boards.models import BoardModel, BoardCompany, Board
from django.db.models import Prefetch




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
        boards_count = dict()
        orders = Order.active_orders.all()
        company_name = BoardCompany.objects.get(code=company_code).name

        for order in orders:
            order_records = OrderRecord.objects.filter(order=order).select_related(
                'board_model')
            for record in order_records:
                model = record.board_model.name
                qty = record.quantity
                code = BoardModel.objects.get(name=model).company.code

                if company_code == code:
                    actual_value = boards_count.get(model, 0)
                    boards_count[model] = actual_value + int(qty)
                    
        sended_boards = SendedBoard.objects.all().select_related('board')
        for sended_board in sended_boards:
            if sended_board.board.company.name == company_name:
                sended_model = sended_board.board.model.name
                if sended_model in boards_count:
                    actual_value = boards_count.get(sended_model, 1)
                    boards_count[sended_model] = actual_value - 1
        return {company_name: boards_count}

    def return_order_info_for_all_companies(self):
        companies = BoardCompany.objects.all()
        companies_list = list()
        for company in companies:
            orders = self.return_order_info(company_code=company.code)
            if not orders[list(orders.keys())[0]] == {}:
                companies_list.append(orders)
        return companies_list

    def add_order_record(barcode, order_id):
        pass


order_service = OrderService()
