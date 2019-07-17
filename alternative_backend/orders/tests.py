from django.test import TestCase
from .models import (
    Order,
    Client
)
from common.tests import (
    ViewSetBaseTests,
    TestAPI,
    init_test_db,
)
from .serializers import (
    OrderSerializer,
    ClientSerializer
)
from .views import (
    OrderViewSet,
    ClientViewSet,

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


class ClientViewSetTests(ViewSetBaseTests, TestCase):
    def setUp(self):
        self.endpoint = 'clients/'
        self.serializer = ClientSerializer
        self.model = Client
        self.new_data = {'name': 'Piotr Dabrowski',
                         'country': 'Poland',
                         'city': 'Krakow',
                         'post_code': '12-345',
                         'adress': 'Piotra 1/4',
                         'is_company': 'false'}
        self.update_data = {'name': 'Heiko Niemiec'}
        self.detail_view = ClientViewSet.as_view(actions=self.view_actions)
        self.view = ClientViewSet.as_view(actions=self.detail_view_actions)
