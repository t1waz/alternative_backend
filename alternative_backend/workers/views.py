from rest_framework import viewsets
from common.auth import BaseAccess
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Worker
from .serializers import WorkerSerializer, WorkerScanSerializer


class WorkerViewSet(viewsets.ModelViewSet):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()
    permission_classes = [BaseAccess]


class NewWorkerScanAPIView(APIView):
    permission_classes = (BaseAccess,)

    def post(self, request, format=None):
        new_worker_scan = WorkerScanSerializer(data=request.data)
        if new_worker_scan.is_valid():
            new_worker_scan.save()
            response = "added worker barcode: %s" % (new_worker_scan.data['worker_barcode'])
        else:
            response = "worker barcode meta data not is_valid"
        return Response(response)
