from rest_framework import viewsets

from common.auth import BaseAccess
from stations.models import Station
from stations.serializers import StationSerializer


class StationViewSet(viewsets.ModelViewSet):
    serializer_class = StationSerializer
    queryset = Station.objects.all()
    permission_classes = [BaseAccess]
