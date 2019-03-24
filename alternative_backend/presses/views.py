from rest_framework import viewsets
from common.auth import BaseAccess
from .models import Press
from .serializers import PressSerializer


class PressViewSet(viewsets.ModelViewSet):
    serializer_class = PressSerializer
    queryset = Press.objects.all()
    permission_classes = [BaseAccess]


