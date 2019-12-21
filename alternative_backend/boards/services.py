from django.db import transaction
from stations.models import Station
from orders.models import SendedBoard
from common.exceptions import ServiceException
from boards.models import (
    Board,
    Layout,
    BoardScan,
    BoardModel,
    BoardGraphic,
    BoardCompany,
    BoardModelMaterial,
)


class BoardService:
    LAYOUT_VALUES = ['layout__top_material__price', 
                     'layout__top_material__currency__price', 'layout__bottom_material__price', 
                     'layout__bottom_material__currency__price', 'layout__top_material',
                     'layout__bottom_material']

    def get_company_from_barcode(self, barcode):
        return BoardCompany.objects.filter(code=str(barcode)[4:6]).first()

    def get_model_from_barcode(self, barcode):
        return BoardModel.objects.filter(code=str(barcode)[2:4],
                                         company__code=str(barcode)[4:6]).first()

    def get_layout(self, **kwargs):
        try:
            layout, is_created = Layout.objects.get_or_create(**kwargs)
        except:  # TODO
            raise ServiceException('layout data incorrect')

        return layout

    @transaction.atomic
    def add_missing_scans(self, last_scan):
        missing_board_scans = []
        station = last_scan.get('station')
        barcode = last_scan.get('barcode')
        prev_stations = Station.objects.filter(
            id__in=range(station.id - 1, 0, -1)).values_list('id', flat=True)
        exists_scans = {station: barcode for station, barcode in 
                        BoardScan.objects.filter(barcode=barcode,
                                                 station_id__in=prev_stations).values_list(
                                                 'station__id', 'barcode__barcode')}

        for station in prev_stations:
            if not exists_scans.get(station):
                missing_board_scans.append(BoardScan(barcode=barcode,
                                                     worker=last_scan.get('worker'),
                                                     station_id=station,
                                                     comment="added automatic"))

        try:   
            BoardScan.objects.bulk_create(missing_board_scans)
        except:    # TODO
            raise ServiceException('cannot create missing scan')

    @transaction.atomic
    def create_new_board(self, **kwargs):
        layout_data = kwargs.pop('layout', None)
        barcode = kwargs.get('barcode')
        model = self.get_model_from_barcode(barcode=barcode)

        if layout_data:
            layout = self.get_layout(**layout_data)
        else:
            layout = model.layout

        try:
            new_board = Board.objects.create(barcode=barcode,
                                             model=model,
                                             company=model.company,
                                             layout=layout,
                                             second_category=False)
        except Exception as e:    # TODO
            raise ServiceException('cannot create new board', e)

        return new_board

    @transaction.atomic
    def create_new_model(self, **kwargs):
        layout_data = kwargs.pop('layout')
        kwargs['layout'] = BoardService().get_layout(**layout_data)
        try:
            new_model = BoardModel.objects.create(**kwargs)
        except Exception as e:    # TODO
            raise ServiceException('cannot create new model', e)

        return new_model

    def get_production_for(self, company_code):
        scan_data = {}
        barcode_model = {}
        company_models = BoardModel.objects.filter(company__code=company_code).values_list(
                                                                            'name', flat=True)
        production = {station_name: {model: 0 for model in company_models} for 
                      station_name, step in Station.objects.all().values_list(
                        'name', 'production_step') if step != 1}
        station_step_names = {int(step): name for step, name in Station.objects.all().values_list(
            'production_step', 'name')}
        last_production_station = Station.objects.all().values_list(
            'production_step', flat=True).order_by('production_step').last()
        data = BoardScan.objects.filter(barcode__company__code=company_code).select_related(
            'barcode', 'station').values_list('barcode__barcode', 'barcode__model__name', 
                                              'station__production_step')
        for barcode, model, station_step in data:
            scan_data[barcode] = max(scan_data.get(barcode, 0), station_step)
            barcode_model[barcode] = model

        for barcode, step in scan_data.items():
            if step != last_production_station:
                station_name = station_step_names[step + 1]
                current_step_data = production[station_name] 
                current_step_data[barcode_model[barcode]] += 1
                production[station_name] = current_step_data

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

    def create_board_model(self, validated_data: dict) -> None:
        return BoardModel.objects.create(**validated_data)

    @transaction.atomic
    def create_components(self, model: BoardModel, components: dict):
        new_components = [BoardModelMaterial(quantity=component.get('quantity'),
                                             material=component.get('material'),
                                             model=model) for 
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

    def get_layout_initial_data_for_model(self, model):
        return BoardModel.objects.filter(id=model.id).values_list(
                *self.LAYOUT_VALUES).first()

    def get_layout_initial_data_for_board(self, board):
        if not board.layout:
            return self.get_layout_initial_data_for_model(board.model)
        else:
            return board.layout.values_list(*self.LAYOUT_VALUES).first()

    def get_layout_price(self, initial_data, model):
        if initial_data[4]:
            top_price = initial_data[0] * initial_data[1]
        else:
            top_price = 0

        if initial_data[5]:
            bottom_price = initial_data[2] * initial_data[3]
        else:
            bottom_price = 0

        return model.layout_material_quantity * (top_price + bottom_price)

    def get_components_price(self, model):
        return sum(quantity * price * currency for (quantity, price, currency) in
                   model.components.all().values_list(
                   'quantity', 'material__price', 'material__currency__price'))

    def get_price_for_model(self, model):
        data = self.get_layout_initial_data_for_model(model=model)
        layout_price = self.get_layout_price(initial_data=data,
                                             model=model)

        return self.get_components_price(model=model) + layout_price

    def get_price_for_board(self, board):
        data = self.get_layout_initial_data_for_board(board=board)
        layout_price = self.get_layout_price(initial_data=data,
                                             model=board.model)

        return self.get_components_price(model=board.model) + layout_price

    def get_board_production_history(self, barcode):
        return [f'{station} : {timestamp}' for (station, timestamp) in
                BoardScan.objects.select_related('station').filter(
                    barcode=barcode).values_list('station__name', 'timestamp')]

    def get_board_customer(self, barcode):
        return SendedBoard.objects.select_related('order').filter(
            board=barcode).values_list('order__client__name', flat=True).first() or ''

    def get_graphic_from_name(self, name):
        return BoardGraphic.objects.filter(name=name).first() or None
