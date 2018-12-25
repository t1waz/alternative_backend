from alternative_backend.exceptions import AppException
from stations.models import Station
from .serializers import BoardScanSerializer
from stations.models import Station
from .models import Board, BoardModel, BoardScan
from .serializers import BoardSerializer
from workers.models import Worker


class BoardScansService:

	def _validate_barcode(self, _barcode):
		if not 10000000000000 <= int(_barcode) <=  99999999999999:
	 		raise AppException('barcode number not valid')

		board_model = int(str(_barcode)[2:4])
		board_company = int(str(_barcode)[4:6])

		try:
			model = BoardModel.objects.get(code=board_model)
			assert model.company.id == board_company
		except:
			raise AppException('barcode not valid')

	def _validate_request_data(self,_data):
		if not all(key in _data for key in ('worker', 'station', 'barcode_scan')):
			raise AppException("request data is not valid")

		first_station = Station.objects.get(id=1).name
		station = Station.objects.filter(name=_data['station']).first()
		board = Board.objects.filter(barcode=_data['barcode_scan']).first()
		worker = Worker.objects.filter(username=_data['worker']).first()

		exist = BoardScan.objects.filter(barcode_scan=board,
									  station=station).exists()

		if exist:
			raise AppException("Scan already made")

		if not worker:
			raise AppException("request worker not valid")

		if not station:
			raise AppException("request station not valid")

		if not board:
			if _data['station'] == first_station:
				self._validate_barcode(_data['barcode_scan'])
			else:
				raise AppException("request barcode not started production")

	def _get_board_from_barcode(self,_barcode):
		board_model = int(str(_barcode)[2:4])
		model = BoardModel.objects.get(code=board_model)

		board = { "barcode": _barcode,
				  "model": model.id,
				  "company": model.company.id }

		return board

	def _add_new_board(self, _data):
		new_board = self._get_board_from_barcode(_data['barcode_scan'])
		new_board_record = BoardSerializer(data=new_board)
		if new_board_record.is_valid():
			new_board_record.save()
		else:
			raise AppException("cannot save, very strange")

	def _save_scan(self, _scan_data):
		new_scan = BoardScanSerializer(data=_scan_data)
		if new_scan.is_valid():
			new_scan.save()
		else:
			raise AppException("request data is not valid")

	def _add_missing_scan(self, _request_data):
		station_id = Station.objects.get(name=_request_data['station']).id
		board = Board.objects.filter(barcode=_request_data['barcode_scan']).first()
		for station_number in range(station_id-1,0,-1):
			exist = BoardScan.objects.filter(barcode_scan=board,
									  station=station_number).first()
			if not exist:
				_request_data['station'] = Station.objects.get(id=station_number).name
				print(_request_data['station'])
				self._save_scan(_request_data)

	def add_new_scan(self, request_data):
		self._validate_request_data(request_data)
		if request_data['station'] == Station.objects.get(id=1).name:
			self._add_new_board(request_data)
		self._save_scan(request_data)
		self._add_missing_scan(request_data)
			


board_scan_service = BoardScansService()
