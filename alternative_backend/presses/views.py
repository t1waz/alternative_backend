from rest_framework import viewsets

from common.auth import BaseAccess
from presses.models import Press
from presses.serializers import (
    PressSerializer,
)


class PressViewSet(viewsets.ModelViewSet):
    queryset = Press.objects.all()
    permission_classes = [BaseAccess]
    serializer_class = PressSerializer

    def get_serializer_context(self):
        return {"worker": self.request.user}
