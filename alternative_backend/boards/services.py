from alternative_backend.exceptions import AppException
from .serializers import BoardScanSerializer
from stations.models import Station
from .models import Board, BoardScan, BoardCompany




class BoardService:
    def _save_scan(self, _scan_data):
        new_scan = BoardScanSerializer(data=_scan_data)
        if new_scan.is_valid():
            new_scan.save()
        else:
            raise AppException("request data is not valid")

    def add_missing_scan(self, _request_data):
        station_id = Station.objects.get(name=_request_data['station']).id
        board = Board.objects.filter(barcode=_request_data['barcode_scan']).first()

        for station_number in range(station_id-1,0,-1):
            scan = BoardScan.objects.filter(barcode_scan=board,
                                            station=station_number).first()
            if not scan:
                _request_data['station'] = Station.objects.get(id=station_number).name
                self._save_scan(_request_data)

    def get_all_barcodes_info(self):
        return Board.objects.all()

    def get_barcode_info(self, barcode):
        return Board.objects.get(barcode=barcode)

    def get_production_for_company(self, company_code):
        production_dict = dict()
        stations = list(Station.objects.all().values_list('name', flat=True))
        for station in stations:
            production_dict[station] = {}
        scans = BoardScan.objects.all().select_related('barcode_scan','station')
        for scan in scans:
            if scan.barcode_scan.company_code == company_code:
                current_station_name = scan.station.name
                current_station_id = scan.station.id
                can_add = True
                if current_station_id > 1:
                    previous_station_id = Station.objects.get(id=current_station_id-1).id
                    if BoardScan.objects.filter(station=previous_station_id, barcode_scan=scan.barcode_scan.id).exists():
                        can_add = False
                current_dict = production_dict[current_station_name]
                current_value = current_dict.get(scan.barcode_scan.model, 0)
                if can_add:
                    current_dict[scan.barcode_scan.model] = current_value + 1

        print(production_dict)


board_service = BoardService()

