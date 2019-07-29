from .models import Press
from .views import PressViewSet
from django.test import TestCase
from .serializers import PressSerializer
from common.tests import (
    ViewSetBaseTests,
    TestAPI,
    init_test_db,
)


class PressViewSetTests(ViewSetBaseTests, TestCase):
    def setUp(self):
        self.endpoint = 'presses/'
        self.serializer = PressSerializer
        self.model = Press
        self.new_data = {'name': 'CZARNA STARA', 
                         'press_time': 7200,
                         'mold': 'Fantail'}
        self.update_data = {'mold': 'Erget'}
        self.detail_view = PressViewSet.as_view(actions=self.view_actions)
        self.view = PressViewSet.as_view(actions=self.detail_view_actions)
