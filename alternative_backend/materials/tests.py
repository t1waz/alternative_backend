from common.utils import ViewSetTestsMixin
from django.test import (
    TestCase,
    override_settings,
)
from materials.views import (
    MaterialViewSet,
    MaterialCategoryViewSet,
)
from materials.serializers import (
    MaterialSerializer,
    MaterialCategorySerializer,
)
from materials.models import (
    Material,
    MaterialCategory,
)


@override_settings(MAX_NUMBER_OF_TOKENS=10000)
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
        {
            'name': 'water like materials',
        },
        {
            'description': 'test description'
        }
    ]
    update_invalid_datas = [

    ]


@override_settings(MAX_NUMBER_OF_TOKENS=10000)
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
        {
            'price': 2
        },
        {
            'name': 'new test name'
        },
    ]
    post_invalid_datas = [
        {
            'description': 'test description',
            'price': 1,
            'name': 'test name',
            'unit': 'pcs',
            'category': 'WOOD',
        },
        {
            'description': 'test description',
            'price': 1,
            'name': 'test name',
            'unit': 'pcs',
            'currency': 'USD',
        },
        {
            'description': 'test description',
            'price': 1,
            'name': 'test name',
            'category': 'WOOD',
            'currency': 'USD',
        },
        {
            'description': 'test description',
            'price': 1,
            'unit': 'pcs',
            'category': 'WOOD',
            'currency': 'USD',
        },
        {
            'description': 'test description',
            'name': 'test name',
            'unit': 'pcs',
            'category': 'WOOD',
            'currency': 'USD',
        },
        {
            'price': 1,
            'name': 'test name',
            'unit': 'pcs',
            'category': 'WOOD',
            'currency': 'USD',
        },
        {
            'description': 'test description',
            'price': 'a',
            'name': 'test name',
            'unit': 'pcs',
            'category': 'WOOD',
            'currency': 'USD',
        },
        {
            'description': 'test description',
            'price': 1,
            'name': 'test name',
            'unit': 'random',
            'category': 'WOOD',
            'currency': 'USD',
        },
        {
            'description': 'test description',
            'price': 1,
            'name': 'test name',
            'unit': 'pcs',
            'category': 1.2,
            'currency': 'USD',
        },
        {
            'description': 'test description',
            'price': 1,
            'name': 'test name',
            'unit': 'pcs',
            'category': 'WOOD',
            'currency': 2.1,
        },

    ]
    update_invalid_datas = [
        {
            'pk': 1,
            'price': 'aaaa',
        },
        {
            'pk': 1,
            'unit': 'none',
        },
        {
            'pk': 1,
            'category': 'none',
        },
        {
            'pk': 1,
            'currency': 'none',
        },
    ]
