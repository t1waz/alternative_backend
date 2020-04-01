from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

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
from materials.services import MaterialService


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


class MaterialStock(APIView):
    permission_classes = (BaseAccess,)

    def get(self, request, format=None):
        response = MaterialService().get_material_stock_info()

        return Response(response)
