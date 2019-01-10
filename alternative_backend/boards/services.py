from alternative_backend.exceptions import AppException
from .serializers import BoardScanSerializer
from stations.models import Station
from .models import Board, BoardScan




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


board_service = BoardService()


class BoardProductionService:

    def get_production(self):
        pass


board_production_service = BoardProductionService()
