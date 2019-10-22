from workers.models import Worker
from common.auth import BaseAccess
from rest_framework import viewsets
from rest_framework.views import APIView
from workers.services import WorkerService
from rest_framework.response import Response
from workers.serializers import (
    WorkerSerializer,
    WorkerScanSerializer,
)


class WorkerLoginAPIView(APIView):
    def post(self, request, format=None):
        token = WorkerService().get_token(username=request.data.get('username'),
                                          password=request.data.get('password'))

        if not token:
            return Response('invalid login data',
                            status=404)

        return Response({'token': token})


class WorkerViewSet(viewsets.ModelViewSet):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()
    permission_classes = [BaseAccess]


class NewWorkerScanAPIView(APIView):
    """
    request data structure: 
                            {
                                "worker_barcode": barcode:int,
                                "started": true/false is started:boolean
                            } 
    comment key is not required
    """
    permission_classes = (BaseAccess,)

    def post(self, request, format=None):
        new_worker_scan = WorkerScanSerializer(data=request.data)
        if new_worker_scan.is_valid():
            new_worker_scan.save()
            response = "added worker barcode: {}".format(new_worker_scan.data['worker_barcode'])
        else:
            response = "worker barcode meta data not is_valid"
        return Response(response)
