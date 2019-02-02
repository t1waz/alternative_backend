from rest_framework import viewsets
from .models import Order, SendedBoard
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
        if new_send_board.is_valid():
            new_send_board.save()
            response = "added sendedboard"
        else:
            response = "scan data not valid"

        return Response(response)
    """
    request data structure: 
                            {
                                "board": barcode:int,
                            } 
    comment key is not required
    """
    def delete(self, request, format=None):
        try:
            sended_board = SendedBoard.objects.get(
                board__barcode=request.data.get('board',0))
            sended_board.delete()
            response = 'barcode removed from order'
        except:
            response = 'something wrong'
        return Response(response)

