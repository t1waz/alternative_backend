from rest_framework import viewsets
from .models import Order
from common.auth import BaseAccess
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import OrderService
from .serializers import (
    OrderSerializer,
    SendedBoardSerializer
)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [BaseAccess]

    def get_serializer_context(self):
        return {"boards": self.request.data.get('boards', [])}


class CompanyOrderInfoAPIView(APIView):
    permission_classes = [BaseAccess]

    def get(self, request, format=None):
        response = OrderService().return_order_info_for_all_companies()
        return Response(response)


class CompanyOrderInfoDetailAPIView(APIView):
    permission_classes = [BaseAccess]

    def get(self, request, code, format=None):
        response = OrderService().return_order_info(company_code=code)
        return Response(response)


class SendedBoardRecordAPIView(APIView):
    permission_classes = [BaseAccess]

    def post(self, request, format=None):
        new_send_board = SendedBoardSerializer(data=request.data)
        if new_send_board.is_valid():
            new_send_board.save()
            response = "added sendedboard"
        else:
            response = "scan data not valid"

        return Response(response)
