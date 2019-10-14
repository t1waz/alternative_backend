from collections import Counter
from django.db import transaction
from stations.models import Station
from orders.models import SendedBoard
from common.exceptions import ServiceException
from .models import (
    Board,
    BoardScan,
    BoardCompany,
    BoardModel
)


class BoardService:
    @transaction.atomic
    def add_missing_scans(self, last_scan):
        station = last_scan.get('station')
        board = last_scan.get('barcode')
        worker = last_scan.get('worker')
        prev_stations = Station.objects.filter(id__in=range(station.id - 1, 0, -1))
        missing_board_scans = []
        for station in prev_stations:
            if not BoardScan.objects.filter(barcode=board,
                                            station=station).exists():
                missing_board_scan = BoardScan(barcode=board,
                                               worker=worker,
                                               station=station,
                                               comment="added automatic")
                missing_board_scans.append(missing_board_scan)

        try:   
            BoardScan.objects.bulk_create(missing_board_scans)
        except:    # TODO
            raise ServiceException('cannot create missing scan')

    def get_barcode_company(self, barcode):    # TODO - if barcode is None
        try:
            return BoardCompany.objects.get(code=str(barcode)[4:6])
        except BoardCompany.DoesNotExist:
            return None
        except Exception:
            raise ServiceException('incorrect input data')

    def get_model_from_barcode(self, barcode):
        try:
            return BoardModel.objects.get(code=str(barcode)[2:4],
                                          company__code=str(barcode)[4:6])
        except BoardModel.DoesNotExist:
            return None
        except:
            raise ServiceException('incorrect input data')

    def create_new_board_from_barcode(self, barcode):
        try:
            new_board = Board.objects.create(barcode=barcode,
                                             model=self.get_model(barcode=barcode),
                                             company=self.get_barcode_company(barcode=barcode),
                                             second_category=False)
        except:    # TODO
            raise ServiceException('cannot create new board')

        return new_board

    def get_production_for(self, company_code):
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
        return {c.name: self.get_production_for(c.code) for c in BoardCompany.objects.all()}

    def get_stock_for(self, company_code):
        stock_dict = dict()
        models = BoardModel.objects.filter(company=company_code).values('name')
        for model in [m['name'] for m in models]:
            finisied = BoardScan.objects.filter(station=Station.objects.latest('id').id,
                                                barcode__company__code=company_code,
                                                barcode__model__name=model).count() or 0
            sended = SendedBoard.objects.filter(board__company__code=company_code,
                                                board__model__name=model).count() or 0
            stock_dict[model] = finisied - sended

        return stock_dict

    def get_stock(self):
        return {c.name: self.get_stock_for(c.code) for c in BoardCompany.objects.all()}
