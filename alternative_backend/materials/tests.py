from django.test import TestCase
from materials.views import (
    MaterialCategoryViewSet,
    MaterialViewSet,
)
from materials.serializers import (
    MaterialCategorySerializer,
    MaterialSerializer,
)
from materials.models import (
    MaterialCategory,
    Material,
)
from common.utils import (
    ViewSetTestsMixin,
)


class MaterialCategoryViewSetTests(ViewSetTestsMixin, TestCase):
    model = MaterialCategory
    endpoint = 'material_categories/'
    view = MaterialCategoryViewSet
    serializer = MaterialCategorySerializer
    post_datas = [
        {
            'name': 'water like materials',
            'description': 'test description'
        },
    ]
    update_datas = [
        {
            'name': 'melon like materials'
        }
    ]
    post_invalid_datas = [

    ]
    update_invalid_datas = [

    ]


class MaterialViewSetTests(ViewSetTestsMixin, TestCase):
    model = Material
    endpoint = 'materials/'
    view = MaterialViewSet
    serializer = MaterialSerializer
    post_datas = [
        {
            'description': 'test description',
            'price': 1,
            'name': 'test name',
            'unit': 'pcs',
            'category': 'WOOD',
            'currency': 'USD',
        },
    ]
    update_datas = [
        {
            'description': 'test description 2'
        },
    ]
    post_invalid_datas = [

    ]
    update_invalid_datas = [

    ]
