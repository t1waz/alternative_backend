from django.test import TestCase
from stations.models import Station
from stations.views import StationViewSet
from stations.serializers import StationSerializer
from common.utils import (
    ViewSetTestsMixin,
)


class StationViewSetTests(ViewSetTestsMixin, TestCase):
    model = Station
    endpoint = 'stations/'
    view = StationViewSet
    serializer = StationSerializer
    post_datas = [
        {
            'name': 'LAST ONE STATION', 
            'description': 'test description'
        },
    ]
    update_datas = [
        {
            'name': 'Update name'
        },
    ]
    post_invalid_datas = [

    ]
    update_invalid_datas = [

    ]
