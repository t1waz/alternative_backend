from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StationSerializer
from .services import StationService
from common.auth import BaseAccess

class StationAPIView(APIView):
	permission_classes = (BaseAccess,)

	def get(self, request, format=None):
		stations = StationService().get_stations()
		response = StationSerializer(stations, many=True).data
		return Response(response)