from rest_framework.views import APIView
from common.auth import BaseAccess
from rest_framework.response import Response
from .services import board_scan_service, board_production_service, board_service
from .serializers import BoardSerializer


class BoardScanAPIView(APIView):

	permission_classes = [BaseAccess]

	def post(self, request, format=None):
		
		board_scan_service.add_new_scan(request.data)
		response = "added barcode scan"
		return Response(response)

class ProductionAPIView(APIView):

	permission_classes = [BaseAccess]

	def get(self, request, format=None):
		

		response = board_production_service.get_production()
		return Response(response)

class BarcodeDetailAPIView(APIView):

	permission_classes = [BaseAccess]

	def get(self, request, barcode, format=None):
		board = board_service.get_board(barcode=barcode)
		response = BoardSerializer(board).data
		
		return Response(response)
