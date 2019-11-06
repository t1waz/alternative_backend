from workers.models import Worker
from rest_framework.views import APIView
from workers.services import WorkerService
from rest_framework.response import Response
from common.auth import (
    BaseAccess,
    TokenService,
)
from rest_framework import (
    viewsets,
    generics,
)
from workers.serializers import (
    WorkerSerializer,
    WorkerWorkHistorySerializer,
)


class WorkerLoginAPIView(APIView):
    def post(self, request, format=None):
        token = WorkerService().get_token(username=request.data.get('username'),
                                          password=request.data.get('password'))

        if not token:
            return Response('invalid login data',
                            status=404)

        return Response({'token': token})


class WorkerTokenValidate(APIView):
    def post(self, request, format=None):
        is_valid = TokenService().validate_token(token=request.data.get('token'))
        return Response({'valid': is_valid})


class WorkerViewSet(viewsets.ModelViewSet):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()
    permission_classes = [BaseAccess]


class WorkerWorkHistoryAPIView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        status_code = 400
        status = {
            'status': False
        }
        worker_stamp = WorkerWorkHistorySerializer(data=request.data)
        if worker_stamp.is_valid():
            worker_stamp.create(worker_stamp.validated_data)
            status['status'] = True
            status_code = 200

        return Response(status, status=status_code)
