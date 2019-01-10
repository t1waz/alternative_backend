from rest_framework.views import APIView
from common.auth import BaseAccess
from rest_framework.response import Response
from .services import board_service
from .serializers import BoardSerializer, BoardScanSerializer, \
    BoardPresentationSerializer




class BoardScanAPIView(APIView):
    permission_classes = (BaseAccess,)

    def post(self, request, format=None):
        new_scan = BoardScanSerializer(data=request.data)
        if new_scan.is_valid():
            new_scan.save()
            response = "added barcode scan"
            board_service.add_missing_scan(request.data)
        else:
            response = "scan data not valid"
        return Response(response)


class NewBoardScanAPIView(APIView):
    permission_classes = (BaseAccess,)

    def post(self, request, format=None):
        new_board = BoardSerializer(data=request.data)
        if new_board.is_valid():
            new_board.save()
            response = "added barcode: %s" % (new_board.data['barcode'])
        else:
            response = "barcode already exist"
        return Response(response)


class ProductionAPIView(APIView):
    permission_classes = (BaseAccess,)

    def get(self, request, format=None):
        response = "AAA"
        return Response(response)


class BarcodeInfoAPIView(APIView):
    permission_classes = (BaseAccess,)

    def get(self, request, format=None):
        boards = board_service.get_all_barcodes_info()
        response = BoardPresentationSerializer(boards, many=True).data
        return Response(response)


class BarcodeInfoDetailAPIView(APIView):
    permission_classes = (BaseAccess,)

    def get(self, request, barcode, format=None):
        board = board_service.get_barcode_info(barcode)
        response = BoardPresentationSerializer(board).data
        return Response(response)
