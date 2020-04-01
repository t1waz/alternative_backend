from django.test import (
    TestCase,
    override_settings,
)

from common.utils import ViewSetTestsMixin
from stations.models import Station
from stations.serializers import StationSerializer
from stations.views import StationViewSet


@override_settings(MAX_NUMBER_OF_TOKENS=10000)
class StationViewSetTests(ViewSetTestsMixin, TestCase):
    model = Station
    endpoint = 'stations/'
    view = StationViewSet
    serializer = StationSerializer
    post_datas = [
        {
            'name': 'LAST ONE STATION', 
            'description': 'test description',
            'production_step': 4
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
