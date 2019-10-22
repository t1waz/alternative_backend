from presses.models import Press
from django.test import TestCase
from presses.views import PressViewSet
from presses.serializers import PressSerializer
from common.utils import (
    ViewSetTestsMixin,
)


class PressViewSetTests(ViewSetTestsMixin, TestCase):
    model = Press
    endpoint = 'presses/'
    view = PressViewSet
    serializer = PressSerializer
    post_datas = [

    ]
    update_datas = [
        {
            'press_time': 100
        },
    ]
    post_invalid_datas = [

    ]
    update_invalid_datas = [

    ]
