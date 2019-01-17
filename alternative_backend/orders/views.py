from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from common.auth import BaseAccess
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import order_service


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [BaseAccess]

    def get_serializer_context(self):
        return {"boards": self.request.data.get('boards', [])}


class CompanyOrderInfo(APIView):
    permission_classes = [BaseAccess]

    def get(self, request, format=None):
        response = order_service.return_order_info_for_all_companies()
        return Response(response)


class CompanyOrderInfoDetail(APIView):
    permission_classes = [BaseAccess]

    def get(self, request, code, format=None):
        response = order_service.return_order_info(company_code=code)
        return Response(response)


class OrderRecordAPIView(APIView):
    permission_classes = [BaseAccess]

    def post(self, request, format=None):
        barcode = request.data['barcode']
        order_id = request.data['order']
        response = order_service.add_order_record(barcode=barcode,
                                                  order_id=order_id)
        return Response(response)
