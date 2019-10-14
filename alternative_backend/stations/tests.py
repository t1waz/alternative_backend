from django.test import TestCase
from stations.models import Station
from stations.views import StationViewSet
from stations.serializers import StationSerializer
from common.tests import (
    ViewSetBaseTests,
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
