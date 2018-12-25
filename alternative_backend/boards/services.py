from alternative_backend.exceptions import AppException
from stations.models import Station
from .serializers import BoardScanSerializer
from stations.models import Station
from .models import Board, BoardModel, BoardScan
from .serializers import BoardSerializer

class BoardScansService:

	def _validate_request_data(self,_data):
		if not all(key in _data for key in ('worker', 'station', 'barcode_scan')):
			raise AppException("request data is not valid")

	def _get_barcode(self, _barcode):
		if not 10000000000000 <= int(_barcode) <=  99999999999999:
			raise AppException('barcode too short')

		if Board.objects.filter(barcode=int(_barcode)).exists():
			raise AppException('barcode already in database')

		board_model = int(str(_barcode)[2:4])
		board_company = int(str(_barcode)[4:6])

		try:
			model = BoardModel.objects.get(code=board_model)
			assert model.company.id == board_company
		except:
			raise AppException('barcode not valid')

		board = { "barcode": _barcode,
				  "model": model.id,
				  "company": model.company.id }

		return board

	def _add_new_board(self, _data):
		if _data['station'] == Station.objects.get(id=1).name:
			new_board = self._get_barcode(_data['barcode_scan'])
			new_board_record = BoardSerializer(data=new_board)
			if new_board_record.is_valid():
				new_board_record.save()
			else:
				raise AppException("cannot save, very strange")

	def _validate_scan(self, _scan_data):
		_station = Station.objects.get(name=_scan_data['station'])
		_barcode_scan =  Board.objects.get(barcode=_scan_data['barcode_scan'])
		if BoardScan.objects.filter(station=_station.id,
									barcode_scan=_barcode_scan.id).exists():
			raise AppException("Already scanned")

	def add_new_scan(self, request_data):
		self._validate_scan(request_data)
		self._validate_request_data(request_data)
		self._add_new_board(request_data)
		
		new_scan = BoardScanSerializer(data=request_data)
		if new_scan.is_valid():
			new_scan.save()
		else:
			raise AppException("request data is not valid")
		





board_scan_service = BoardScansService()
