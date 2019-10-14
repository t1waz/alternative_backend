from common.auth import BaseAccess
from .services import BoardService
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    BoardCompany,
    BoardModel,
    BoardScan,
    Board,
)
from .serializers import (
    BoardScanSerializer,
    BoardCompanySerializer,
    BoardModelSerializer,
    BoardListSerializer,
    BoardDetailViewSerializer,
    BoardCreateSerializer,
    BoardUpdateSerializer,
)


class BoardCompanyViewSet(viewsets.ModelViewSet):
    permission_classes = (BaseAccess, )
    queryset = BoardCompany.objects.all()
    serializer_class = BoardCompanySerializer


class BoardModelViewSet(viewsets.ModelViewSet):
    permission_classes = (BaseAccess, )
    queryset = BoardModel.objects.all()
    serializer_class = BoardModelSerializer


class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = (BaseAccess, )
    queryset = Board.objects.all()
    lookup_field = 'barcode'

    def get_serializer_class(self):
        if self.action == 'list':
            return BoardListSerializer
        elif self.action == 'retrieve':
            return BoardDetailViewSerializer
        elif self.action == 'create':
            return BoardCreateSerializer
        elif self.action == 'partial_update':
            return BoardUpdateSerializer


class BoardScanAPIView(generics.CreateAPIView):
    permission_classes = (BaseAccess, )
    queryset = BoardScan.objects.all()
    serializer_class = BoardScanSerializer


class ProductionAPIView(APIView):
    permission_classes = (BaseAccess,)

    def get(self, request, format=None):
        response = BoardService().get_production()

        return Response(response)


class ProductionDetailAPIView(APIView):
    permission_classes = (BaseAccess,)

    def get(self, request, company, format=None):
        response = BoardService().get_production_for(company_code=company)

        return Response(response)


class StockAPIView(APIView):
    permission_classes = (BaseAccess,)

    def get(self, request, format=None):
        response = BoardService().get_stock()

        return Response(response)


class StockDetailAPIView(APIView):
    permission_classes = (BaseAccess,)

    def get(self, request, code, format=None):
        response = BoardService().get_stock_for(company_code=code)

        return Response(response)
