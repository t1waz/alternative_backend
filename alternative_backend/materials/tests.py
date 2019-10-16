from django.test import TestCase
from common.tests import (
    ViewSetBaseTests,
)
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


class MaterialCategoryViewSetTests(ViewSetBaseTests, TestCase):
    def setUp(self):
        self.endpoint = 'material_categories/'
        self.serializer = MaterialCategorySerializer
        self.model = MaterialCategory
        self.new_data = {
        	'name': 'water like materials',
        	'description': 'test description'
        }
        self.update_datas = [
        	{
        		'name': 'melon like materials'
        	}
        ]
        self.detail_view = MaterialCategoryViewSet.as_view(actions=self.view_actions)
        self.view = MaterialCategoryViewSet.as_view(actions=self.detail_view_actions)


class MaterialViewSetTests(ViewSetBaseTests, TestCase):
	def setUp(self):
		self.endpoint = 'materials/'
		self.serializer = MaterialSerializer
		self.model = Material
		self.new_data = {
			'description': 'test description',
			'price': 1,
			'name': 'test name',
			'unit': 'pcs',
			'category': 'WOOD'
		}
		self.update_datas = [
			{
				'description': 'test description 2'
			}
		]
		self.detail_view = MaterialViewSet.as_view(actions=self.view_actions)
		self.view = MaterialViewSet.as_view(actions=self.detail_view_actions)
