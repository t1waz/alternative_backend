from django.test import TestCase
from .models import (
    Order
)
from common.tests import (
    ViewSetBaseTests,
    TestAPI,
    init_test_db,
)
from .serializers import (
    OrderSerializer
)
from .views import (
    OrderViewSet
)


class OrderViewSetTests(ViewSetBaseTests, TestCase):
    def setUp(self):
        self.endpoint = 'orders/'
        self.serializer = OrderSerializer
        self.model = Order
        self.new_data = {'client': 'Lukasz Tomkiel',
                         'boards': {'Fantail': 2}}
        self.update_data = {'client': 'Heiko'}
        self.detail_view = OrderViewSet.as_view(actions=self.view_actions)
        self.view = OrderViewSet.as_view(actions=self.detail_view_actions)
