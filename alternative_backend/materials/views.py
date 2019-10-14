from rest_framework import viewsets
from common.auth import BaseAccess
from materials.models import (
    MaterialCategory,
    Material,
    BoardModelComponent,
)
from materials.serializers import (
    MaterialCategorySerializer,
    MaterialSerializer,
    BoardModelComponentSerializer,
)


class MaterialCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (BaseAccess, )
    queryset = MaterialCategory.objects.all()
    serializer_class = MaterialCategorySerializer


class MaterialViewSet(viewsets.ModelViewSet):
    permission_classes = (BaseAccess, )
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
