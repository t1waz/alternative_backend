from collections import Counter
from stations.models import Station
from orders.models import SendedBoard
from workers.models import Worker
from .models import (
    Board,
    BoardScan,
    BoardCompany,
    BoardModel
)


class BoardService:
    def add_missing_scan(self, _request_data):
        station = Station.objects.get(name=_request_data['station'])
        board = Board.objects.get(barcode=_request_data['barcode'])
        worker = Worker.objects.get(username=_request_data['worker'])

        prev_stations = Station.objects.filter(id__in=range(station.id - 1, 0, -1))

        for station in prev_stations:
            if not BoardScan.objects.filter(barcode=board,
                                            station=station).exists():
                BoardScan.objects.create(barcode=board,
                                         worker=worker,
                                         station=station,
                                         comment="added automatic")

    def get_all_barcodes(self):
        return Board.objects.all()

    def get_barcode(self, barcode):
        return Board.objects.get(barcode=barcode)

    def get_production_for(self, company_code):
        company = BoardCompany.objects.get(code=company_code)
        stations = [station.name for station in Station.objects.all()]
        scans = BoardScan.objects.filter(barcode__company=company).select_related(
            'barcode', 'station').order_by('station_id')
        boards_model = [board.name for board in BoardModel.objects.filter(
                        company__code=company_code)]
        production = {}
        for i, station in enumerate(stations[:-1]):
            production[stations[i + 1]] = \
                Counter([s.barcode.model.name for s in scans if s.station.name == station]) - \
                Counter([s.barcode.model.name for s in scans if s.station.name == stations[i + 1]])
            # adding zero values to nice data presentation. ELO
            for model in boards_model:
                if model not in production[stations[i + 1]].keys():
                    production[stations[i + 1]][model] = 0                                          

        return production

    def get_production(self):
        return {c.name: self.get_production_for(c.code) for c in BoardCompany.objects.all()}

    def get_stock_for(self, company_code):
        stock_dict = dict()
        for model in [m.name for m in BoardModel.objects.filter(company=company_code)]:
            finisied = BoardScan.objects.filter(station=Station.objects.latest('id').id,
                                                barcode__company__code=company_code,
                                                barcode__model__name=model).count() or 0
            sended = SendedBoard.objects.filter(board__company__code=company_code,
                                                board__model__name=model).count() or 0
            stock_dict[model] = finisied - sended

        return stock_dict

    def get_stock(self):
        return {c.name: self.get_stock_for(c.code) for c in BoardCompany.objects.all()}

    def get_board(self, barcode):
        return Board.objects.filter(barcode=barcode)[0]
