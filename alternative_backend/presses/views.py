from presses.models import Press
from common.auth import BaseAccess
from rest_framework import viewsets
from rest_framework.views import APIView
from presses.services import PressService
from rest_framework.response import Response
from common.exceptions import ServiceException
from presses.serializers import (
    PressSerializer,
    MoldHistorySerializer,
)


class PressViewSet(viewsets.ModelViewSet):
    serializer_class = PressSerializer
    queryset = Press.objects.all()
    permission_classes = [BaseAccess]


class MoldChangeApiView(APIView):
    permission_classes = (BaseAccess,)

    def post(self, request, format=None):
        response = Response(status=400)
        history = MoldHistorySerializer(data=request.data)

        if history.is_valid(raise_exception=True):
            data = history.validated_data
            try:
                status = PressService().handle_history(worker=data['worker'], 
                                                       press=data['press'], 
                                                       mold=data['mold'])
            except ServiceException:
                response.status = 500
                response.data = "internal error"

            if status:
                response.status = 201
                response.data = "mold changed"
            else:
                response.data = "cannot change mold to the same"

        return response
