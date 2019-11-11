from django.db.models import Q
from collections import Counter
from django.db import transaction
from stations.models import Station
from orders.models import SendedBoard
from common.exceptions import ServiceException
from boards.models import (
    Board,
    BoardScan,
    BoardModel,
    BoardGraphic,
    BoardCompany,
    BoardModelMaterial,
    BoardModelLayout,
)


class BoardService:
    def get_company_from_barcode(self, barcode):
        return BoardCompany.objects.filter(code=str(barcode)[4:6]).first() or None

    def get_model_from_barcode(self, barcode):
        try:
            return BoardModel.objects.filter(code=str(barcode)[2:4],
                                             company__code=str(barcode)[4:6]).first() or None
        except: 
            return None

    def get_model_from_name(self, model_name):
        return BoardModel.objects.filter(name=model_name).first() or None

    def get_model_from_pk(self, model_pk):
        return BoardModel.objects.filter(id=model_pk).first() or None

    def get_layout(self, **kwargs):
        try:
            layout, is_created = BoardModelLayout.objects.get_or_create(**kwargs)
        except:  # TODO
            raise ServiceException('layout data incorrect')

        return layout

    @transaction.atomic
    def add_missing_scans(self, last_scan: dict) -> None:
        missing_board_scans = []
        station = last_scan.get('station')
        barcode = last_scan.get('barcode')
        prev_stations = Station.objects.filter(
            id__in=range(station.id - 1, 0, -1)).values_list('id', flat=True)

        for station in prev_stations:
            if not BoardScan.objects.filter(barcode=barcode,
                                            station_id=station).exists():
                missing_board_scans.append(BoardScan(barcode=barcode,
                                                     worker=last_scan.get('worker'),
                                                     station_id=station,
                                                     comment="added automatic"))

        try:   
            BoardScan.objects.bulk_create(missing_board_scans)
        except:    # TODO
            raise ServiceException('cannot create missing scan')

    @transaction.atomic
    def create_new_board(self, barcode, **kwargs):
        model = self.get_model_from_barcode(barcode=barcode)

        if all(value is None for value in kwargs.values()):
            layout = model.layout
        else:
            layout = BoardService().get_layout(**kwargs)

        try:
            new_board = Board.objects.create(barcode=barcode,
                                             model=model,
                                             company=model.company,
                                             layout=layout,
                                             second_category=False)
        except Exception as e:    # TODO
            raise ServiceException('cannot create new board', e)

        return new_board

    def get_production_for(self, company_code: str) -> dict:
        company = BoardCompany.objects.get(code=company_code)
        stations = list(Station.objects.all().values_list('name', flat=True))
        scans = BoardScan.objects.filter(barcode__company=company).select_related(
            'barcode', 'station').order_by('station_id')
        boards_model = [board['name'] for board in BoardModel.objects.filter(
                        company__code=company_code).values('name')]
        production = {}
        for i, station in enumerate(stations[:-1]):
            production[stations[i + 1]] = \
                Counter([s.barcode.model.name for s in scans if s.station.name == station]) - \
                Counter([s.barcode.model.name for s in scans if s.station.name == stations[i + 1]])
            # Adding zero values to nice data presentation.
            for model in boards_model:
                if model not in production[stations[i + 1]].keys():
                    production[stations[i + 1]][model] = 0                                          

        return production

    def get_production(self):
        return {name: self.get_production_for(code) for name, code in 
                BoardCompany.objects.all().values_list('name', 'code')}

    def get_stock_for(self, company_code: str) -> dict:
        stock_dict = dict()
        models = BoardModel.objects.filter(company=company_code).values_list('name', flat=True)

        for model in models:
            finisied = BoardScan.objects.filter(station=Station.objects.latest('id').id,
                                                barcode__company__code=company_code,
                                                barcode__model__name=model).count() or 0
            sended = SendedBoard.objects.filter(board__company__code=company_code,
                                                board__model__name=model).count() or 0
            stock_dict[model] = finisied - sended

        return stock_dict

    def get_stock(self):
        return {c.name: self.get_stock_for(c.code) for c in BoardCompany.objects.all()}

    def get_model_construction(self, model_name: str) -> dict:
        return {material: quantity for (material, quantity) in
                BoardModelMaterial.objects.filter(model__name=model_name).values_list(
                    'material__name', 'quantity')}

    def get_model_production_price(self, model_name: str) -> dict:
        return sum(qty * material_price for (qty, material_price) in 
                BoardModelMaterial.objects.filter(model__name=model_name).values_list(
                        'quantity', 'material__price'))

    def create_board_model(self, validated_data: dict) -> None:
        return BoardModel.objects.create(**validated_data)

    @transaction.atomic
    def create_components(self, model: BoardModel, components: dict):
        new_components = [BoardModelMaterial(quantity=component.get('quantity'),
                                             model=model,
                                             material=component.get('material')) for 
                          component in components]
        try:
            BoardModelMaterial.objects.bulk_create(new_components)
        except:  # TODO
            raise ServiceException('internal error - cannot create')

    @transaction.atomic
    def update_components(self, model: BoardModel, components: dict):
        model.components.all().delete()

        self.create_components(model=model,
                               components=components)

    def get_board_model_components(self, board_model_pk):
        return BoardModelMaterial.objects.filter(model__id=board_model_pk)

    def get_layout_price(self, board):
        values = ['layout__material_quantity', 'layout__top_material__price', 
                  'layout__top_material__currency__price', 'layout__bottom_material__price', 
                  'layout__bottom_material__currency__price', 'layout__top_material',
                  'layout__bottom_material']

        if not board.layout:
            raw_data = BoardModel.objects.filter(id=board.model.id).values_list(*values).first()
        else:
            raw_data = board.layout.values_list(*values).first()

        if raw_data[5]:
            top_price = raw_data[1] * raw_data[2]
        else:
            top_price = 0

        if raw_data[6]:
            bottom_price = raw_data[3] * raw_data[4]
        else:
            bottom_price = 0

        return raw_data[0] * (top_price + bottom_price)

    def get_price_for_board(self, board):
        layout_price = self.get_layout_price(board=board)

        return sum(quantity * price * currency for (quantity, price, currency) in
                   board.model.components.all().values_list(
                   'quantity', 'material__price', 'material__currency__price')) + layout_price

    def get_board_production_history(self, barcode):
        return [f'{station} : {timestamp}' for (station, timestamp) in
                BoardScan.objects.select_related('station').filter(
                    barcode=barcode).values_list('station__name', 'timestamp')]

    def get_board_customer(self, barcode):
        try:
            return SendedBoard.objects.select_related('order').filter(
                board=barcode).values_list('order__client__name', flat=True).first() or ''
        except:
            return None

    def get_graphic_from_name(self, name):
        return BoardGraphic.objects.filter(name=name).first() or None
