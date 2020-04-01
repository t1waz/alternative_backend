from django.test import (
    TestCase,
    override_settings,
)

from common.utils import (
    ViewSetTestsMixin,
)
from presses.models import (
    Press,
    MoldHistory,
)
from presses.serializers import PressSerializer
from presses.views import PressViewSet


@override_settings(MAX_NUMBER_OF_TOKENS=10000)
class PressViewSetTests(ViewSetTestsMixin, TestCase):
    model = Press
    endpoint = 'presses/'
    view = PressViewSet
    serializer = PressSerializer
    post_datas = [
        {
            'name': 'prasa testowa',
            'mold': 'Fantail',
            'press_time': 123
        },
    ]
    update_datas = [
        {
            'press_time': 100
        },
        {
            'mold': 'Fantail'
        }
    ]
    post_invalid_datas = [
        {
            'name': 'prasa testowa bez czasu',
            'mold': 'Fantail'
        },
        {
            'name': 'prasa testowa',
            'press_time': 123
        },
        {
            'mold': 'Fantail',
            'press_time': 123
        }
    ]
    update_invalid_datas = [
        {
            'pk': 1,
            'press_time': 'aa'
        },
        {
            'pk': 1,
            'name': 11
        },
        {
            'pk': 1,
            'mold': 22
        }
    ]

    def test_changing_mold(self):
        data = {
            'mold': 'Fantail'
        }
        request = self.api.patch_request(self.endpoint, data)
        response = self.view(request, pk=1)

        assert response.status_code == 200

        mold_name = response.data.get('name')
        new_history = MoldHistory.objects.filter(press__name=mold_name,
                                                 mold__name='Fantail',
                                                 started__isnull=False,
                                                 finished__isnull=True).first()
        old_history = MoldHistory.objects.filter(press__name=mold_name,
                                                 mold__name='Erget',
                                                 started__isnull=False,
                                                 finished__isnull=False).first()

        assert new_history is not None
        assert old_history is not None
