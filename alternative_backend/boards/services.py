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

    def get_all_barcodes(self):
        return Board.objects.all()

    def get_barcode(self, barcode):
        return Board.objects.get(barcode=barcode)

    def get_production_for_company(self, company_id):
        production_dict = dict()
        stations = list(Station.objects.all().values_list('name', flat=True))
        company_id = BoardCompany.objects.get(id=company_id)
        for station in stations[1:]:
            production_dict[station] = {}

        scans = BoardScan.objects.filter(
            barcode_scan__company=company_id).select_related(
            'barcode_scan','station').exclude(station__id=len(stations))
        for scan in scans:
            current_station_scan = scan.station
            next_station_scan = Station.objects.get(id=current_station_scan.id+1)
            next_scan_exists = BoardScan.objects.filter(station=next_station_scan.id,
                                                        barcode_scan=scan.barcode_scan).exists()

            if not next_scan_exists:
                current_dict = production_dict[next_station_scan.name]
                current_value = current_dict.get(scan.barcode_scan.model.name, 0)
                current_dict[scan.barcode_scan.model.name] = current_value + 1

        return production_dict

    def get_production(self):
        companies = BoardCompany.objects.all()
        production_dict = dict()
        for company in companies:
            production_dict[company.name] = self.get_production_for_company(company.id)

        return production_dict


board_service = BoardService()

