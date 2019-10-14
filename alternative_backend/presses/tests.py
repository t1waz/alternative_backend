from presses.models import Press
from django.test import TestCase
from presses.views import PressViewSet
from presses.serializers import PressSerializer
from common.tests import (
    ViewSetBaseTests,
)


class PressViewSetTests(ViewSetBaseTests, TestCase):
    def setUp(self):
        self.endpoint = 'presses/'
        self.serializer = PressSerializer
        self.model = Press
        self.new_data = {'name': 'CZARNA STARA', 
                         'press_time': 7200}
        self.update_datas = [{'press_time': 100}]
        self.detail_view = PressViewSet.as_view(actions=self.view_actions)
        self.view = PressViewSet.as_view(actions=self.detail_view_actions)
