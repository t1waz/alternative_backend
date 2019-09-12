from .models import Station
from django.test import TestCase
from .views import StationViewSet
from .serializers import StationSerializer
from common.tests import (
    ViewSetBaseTests,
    TestAPI,
    init_test_db,
)


class StationViewSetTests(ViewSetBaseTests, TestCase):
    def setUp(self):
        self.endpoint = 'stations/'
        self.serializer = StationSerializer
        self.model = Station
        self.new_data = {'name': 'LAST ONE STATION', 
                         'description': 'test description'}
        self.update_datas = [{'name': 'Update name'}]
        self.detail_view = StationViewSet.as_view(actions=self.view_actions)
        self.view = StationViewSet.as_view(actions=self.detail_view_actions)
