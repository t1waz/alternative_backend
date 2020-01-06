from workers.models import Worker
from common.auth import BaseAccess
from rest_framework.views import APIView
from rest_framework.response import Response
from alternative_backend.services import TokenService
from workers.services import WorkerService
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
        token = None
        worker = WorkerService().get_worker(username=request.data.get('username'),
                                            password=request.data.get('password'))
        if not worker:
            return Response('invalid login data',
                            status=404)

        token = TokenService().generate_new_token(username=worker.username)

        if not token:
            return Response('too many tokens',
                            status=429)

        return Response({'token': token})


class WorkerLogoutAPIView(APIView):
    permission_classes = (BaseAccess,)

    def get(self, request, format=None):
        TokenService().revoke_user_tokens(username=request.user.username)

        return Response('logout completed')


class WorkerTokenValidate(APIView):
    def post(self, request, format=None):
        is_valid = TokenService().validate_token(token=request.data.get('token'))
        return Response({'valid': is_valid})


class WorkerViewSet(viewsets.ModelViewSet):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()
    permission_classes = [BaseAccess]


class WorkerWorkHistoryAPIView(generics.CreateAPIView):
    permission_classes = (BaseAccess,)

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
