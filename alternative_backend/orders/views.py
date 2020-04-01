from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from common.auth import BaseAccess
from orders.models import (
    Order,
    Client,
    SendedBoard,
)
from orders.serializers import (
    OrderSerializer,
    ClientSerializer,
    SendedBoardSerializer,
    DeleteSendedSerializer,
)
from orders.services import OrderService


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [BaseAccess]


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [BaseAccess]


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


class SendedBoardRecordAPIView(mixins.CreateModelMixin,
                               generics.GenericAPIView):
    permission_classes = (BaseAccess, )
    queryset = SendedBoard.objects.all()
    serializer_class = SendedBoardSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        sended_board = DeleteSendedSerializer(data=request.data)
        if sended_board.is_valid(raise_exception=True):
            return Response('barcode removed from order')
