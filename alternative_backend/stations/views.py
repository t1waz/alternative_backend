from rest_framework import viewsets
from .serializers import StationSerializer
from .models import Station
from common.auth import BaseAccess


class StationViewSet(viewsets.ModelViewSet):
    serializer_class = StationSerializer
    queryset = Station.objects.all()
    permission_classes = [BaseAccess]
