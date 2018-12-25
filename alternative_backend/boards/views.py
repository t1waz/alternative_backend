from rest_framework.views import APIView
from .models import BoardScan, Board
from .serializers import BoardScanSerializer, BoardSerializer
from common.auth import BaseAccess
from rest_framework.response import Response
from .services import board_scan_service

from rest_framework import viewsets

class BoardScanAPIView(APIView):

	permission_classes = [BaseAccess]

	def post(self, request, format=None):
		
		board_scan_service.add_new_scan(request.data)
		response = ""
		return Response(response)


