from rest_framework import viewsets
from common.auth import BaseAccess
from rest_framework.views import APIView
from rest_framework.response import Response
from alternative_backend.exceptions import AppException
from .services import OrderService
from .models import (
    Order, 
    Client
)
from .serializers import (
    OrderSerializer,
    SendedBoardSerializer,
    ClientSerializer,
    DeleteSendedSerializer,
)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [BaseAccess]

    def get_serializer_context(self):
        extra_content = {"boards": self.request.data.get('boards', {}),
                         "request_method": self.request.method}
        return extra_content


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


class SendedBoardRecordAPIView(APIView):
    """
    request data structure: 
                            {
                                "board": barcode:int,
                                "order": order pk: int
                            } 
    comment key is not required
    """
    permission_classes = [BaseAccess]

    def post(self, request, format=None):
        new_send_board = SendedBoardSerializer(data=request.data)
        if new_send_board.is_valid(raise_exception=True):
            new_send_board.save()
            return Response('added sendedboard')
        
    """
    request data structure: 
                            {
                                "board": barcode:int,
                                "order": order pk:int,
                            } 
    comment key is not required
    """
    def delete(self, request, format=None):
        sended_board = DeleteSendedSerializer(data=request.data)
        if sended_board.is_valid(raise_exception=True):
            return Response('barcode removed from order')
