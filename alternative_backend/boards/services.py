from stations.models import Station
from orders.models import SendedBoard
from workers.models import Worker
from .models import Board, BoardScan, BoardCompany, BoardModel



class BoardService:
    def add_missing_scan(self, _request_data):
        station = Station.objects.get(name=_request_data['station'])
        board = Board.objects.get(barcode=_request_data['barcode'])
        worker = Worker.objects.get(username=_request_data['worker'])

        previous_stations = Station.objects.filter(id__in=range(station.id-1,0,-1))

        for station in previous_stations:
            scan = BoardScan.objects.filter(barcode=board,
                                            station=station).exists()
            if not scan:
                BoardScan.objects.create(barcode=board,
                                         worker=worker,
                                         station=station,
                                         comment="added automatic")

    def get_all_barcodes(self):
        return Board.objects.all()

    def get_barcode(self, barcode):
        return Board.objects.get(barcode=barcode)

    def get_production_for_company(self, company_code):
        production_dict = dict()
        stations = list(Station.objects.all().values_list('name', flat=True))
        company = BoardCompany.objects.get(code=company_code)
        for station in stations[1:]:
            production_dict[station] = {}

        scans = BoardScan.objects.filter(barcode__company=company).select_related(
                                         'barcode_scan','station').exclude(station__id=len(stations))
        for scan in scans:
            current_station_scan = scan.station
            next_station_scan = Station.objects.get(id=current_station_scan.id+1)
            next_scan_exists = BoardScan.objects.filter(station=next_station_scan.id,
                                                        barcode=scan.barcode_scan).exists()

            if not next_scan_exists:
                current_dict = production_dict[next_station_scan.name]
                current_value = current_dict.get(scan.barcode_scan.model.name, 0)
                current_dict[scan.barcode_scan.model.name] = current_value + 1

        return production_dict

    def get_production(self):
        companies = BoardCompany.objects.all()
        production_dict = dict()

        for company in companies:
            production_dict[company.name] = self.get_production_for_company(company.code)

        return production_dict

    def get_stock_for_company(self, company_code):
        stock_dict = dict()
        company = BoardCompany.objects.get(code=company_code)
        board_models = BoardModel.objects.filter(company=company_code).values_list(
                                                 'name', flat=True)

        for model in board_models:
            stock_dict[model] = 0
        last_station_id = max(list(Station.objects.all().values_list('id', flat=True)))
        finisied_boards = BoardScan.objects.filter(station=last_station_id,
                                                   barcode__company=company).values_list(
                                                   'barcode_scan', flat=True)
        sended_boards = SendedBoard.objects.all().values_list('board')

        stock_boards = finisied_boards.difference(sended_boards)
        
        for board in stock_boards:
            current_board = Board.objects.get(id=board)
            current_model = current_board.model.name
            current_dict_value = stock_dict.get(current_model,0)
            stock_dict[current_model] = current_dict_value + 1
   
        return stock_dict

    def get_stock(self):
        companies = BoardCompany.objects.all()
        production_dict = dict()
        for company in companies:
            production_dict[company.name] = self.get_stock_for_company(company.code)

        return production_dict




board_service = BoardService()

