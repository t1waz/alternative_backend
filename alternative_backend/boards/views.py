from rest_framework.views import APIView
from common.auth import BaseAccess
from rest_framework.response import Response
from .services import BoardService
from rest_framework import viewsets
from .models import (
    BoardCompany,
    BoardModel,
)
from .serializers import (
    BoardSerializer,
    BoardScanSerializer,
    BoardCompanySerializer,
    BoardPresentationSerializer,
    BoardSecondCategorySerializer,
    BoardModelSerializer,
)


class BoardCompanyViewSet(viewsets.ModelViewSet):
    serializer_class = BoardCompanySerializer
    queryset = BoardCompany.objects.all()
    permission_classes = [BaseAccess]


class BoardModelViewSet(viewsets.ModelViewSet):
    serializer_class = BoardModelSerializer
    queryset = BoardModel.objects.all()
    permission_classes = [BaseAccess]


class BoardScanAPIView(APIView):
    """
    request data structure: 
                            {
                                "barcode": barcode:int,
                                "worker": worker:str,      (username)
                                "station": station:str,    (name)
                                "comment": comment:str,
                            } 
    comment key is not required
    """
    permission_classes = (BaseAccess,)

    def post(self, request, format=None):
        new_scan = BoardScanSerializer(data=request.data)
        if new_scan.is_valid():
            BoardService().add_missing_scan(request.data)
            new_scan.save()
            return Response("ADDED")
        else:
            return Response("DUPLICATED/INCORRECT", status=400)


class NewBoardBarcodeAPIView(APIView):
    """
    request data structure: 
                            {
                                "barcode": barcode:int
                            } 
    all keys are required
    """
    permission_classes = (BaseAccess,)

    def post(self, request, format=None):
        new_board = BoardSerializer(data=request.data)
        if new_board.is_valid():
            new_board.save()
            return Response("added barcode: {}".format(new_board.data['barcode']))
        else:
            return Response("barcode meta data not valid", status=400)


class BoardSecondCategoryAPIView(APIView):
    """
    request data structure: 
                            {
                                "barcode": barcode:int,
                                "second_category": category:boolean
                            } 
    all keys are required
    """
    permission_classes = (BaseAccess,)

    def post(self, request, format=None):
        board = BoardService().get_board(request.data['barcode'])
        if not board:
            return Response("INCORRECT DATA", status=400)
        new_second_board = BoardSecondCategorySerializer(board, data=request.data, )
        if new_second_board.is_valid():
            new_second_board.save()
            return Response("added {}".format(request.data['barcode']))
        else:
            return Response("INCORRECT DATA", status=400)


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
    def get(self, request, format=None):
        response = BoardService().get_stock()
        return Response(response)


class StockDetailAPIView(APIView):
    def get(self, request, code, format=None):
        response = BoardService().get_stock_for(company_code=code)
        return Response(response)


class BarcodeInfoAPIView(APIView):
    permission_classes = (BaseAccess,)

    def get(self, request, format=None):
        boards = BoardService().get_all_barcodes()
        response = BoardPresentationSerializer(boards, many=True).data
        return Response(response)


class BarcodeInfoDetailAPIView(APIView):
    permission_classes = (BaseAccess,)

    def get(self, request, barcode, format=None):
        board = BoardService().get_barcode(barcode)
        response = BoardPresentationSerializer(board).data
        return Response(response)
