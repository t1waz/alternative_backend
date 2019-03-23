from rest_framework.views import APIView
from common.auth import BaseAccess
from rest_framework.response import Response
from .models import Press
from .serializers import PressSerializer
from .services import PressService


class PressAPIView(APIView):
	permission_classes = (BaseAccess,)

	def get(self, request, format=None):
		presses = PressService().get_presses()
		response = PressSerializer(presses, many=True).data
		return Response(response)


class PressDetailAPIView(APIView):
	permission_classes = (BaseAccess,)
	def get(self, request, id, format=None):
		press = PressService().get_press(id)
		response = PressSerializer(press).data
		return Response(response)
