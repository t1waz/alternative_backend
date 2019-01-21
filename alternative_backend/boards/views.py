from rest_framework.views import APIView
from common.auth import BaseAccess
from rest_framework.response import Response
from .services import BoardService
from .serializers import (
    BoardSerializer,
    BoardScanSerializer,
    BoardPresentationSerializer
)


class BoardScanAPIView(APIView):
    permission_classes = (BaseAccess,)

    def post(self, request, format=None):
        new_scan = BoardScanSerializer(data=request.data)
        if new_scan.is_valid():
            BoardService().add_missing_scan(request.data)
            new_scan.save()
            response = "added barcode scan"
        else:
            response = "scan data not valid"
        return Response(response)


class NewBoardScanAPIView(APIView):
    permission_classes = (BaseAccess,)

    def post(self, request, format=None):
        new_board = BoardSerializer(data=request.data)
        if new_board.is_valid():
            new_board.save()
            response = "added barcode: {}".format(new_board.data['barcode'])
        else:
            response = "barcode meta data not is_valid"
        return Response(response)


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
