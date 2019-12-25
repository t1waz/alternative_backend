from rest_framework import viewsets
from common.auth import BaseAccess
from materials.models import (
    Material,
    MaterialDelivery,
    MaterialCategory,
)
from materials.serializers import (
    MaterialSerializer,
    MaterialDeliverySerializer,
    MaterialCategorySerializer,
    MaterialDeliveryDetailedSerializer,
)


class MaterialCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (BaseAccess, )
    queryset = MaterialCategory.objects.all()
    serializer_class = MaterialCategorySerializer


class MaterialViewSet(viewsets.ModelViewSet):
    permission_classes = (BaseAccess, )
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class MaterialDeliveryViewSet(viewsets.ModelViewSet):
    permission_classes = (BaseAccess, )
    queryset = MaterialDelivery.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return MaterialDeliverySerializer
        else:
            return MaterialDeliveryDetailedSerializer
