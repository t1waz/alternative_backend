from django.test import TestCase
from orders.models import (
    Order,
    Client
)
from common.utils import (
    ViewSetTestsMixin,
    init_test_db,
    get_token,
    TestAPI,
)
from orders.serializers import (
    OrderSerializer,
    ClientSerializer
)
from orders.views import (
    OrderViewSet,
    ClientViewSet,
    CompanyOrderInfoAPIView,
    CompanyOrderInfoDetailAPIView,
    SendedBoardRecordAPIView,
)


class OrderViewSetTests(ViewSetTestsMixin, TestCase):
    model = Order
    endpoint = 'orders/'
    view = OrderViewSet
    serializer = OrderSerializer
    post_datas = [
        {
            'client': 'Lukasz Tomkiel',
            'records': [
                {
                    "board_model": "Fantail",
                    "quantity": 2
                }
            ]
        },
    ]
    update_datas = [
        {
            'client': 'Heiko'
        }, 
        {
            'records': [
                {
                    "board_model": "Fantail",
                    "quantity": 22
                }
            ]
        },
    ]
    post_invalid_datas = [

    ]
    update_invalid_datas = [

    ]


class ClientViewSetTests(ViewSetTestsMixin, TestCase):
    model = Client
    endpoint = 'clients/'
    view = ClientViewSet
    serializer = ClientSerializer
    post_datas = [
        {
            'name': 'Piotr Dabrowski',
            'country': 'Poland',
            'city': 'Krakow',
            'post_code': '12-345',
            'adress': 'Piotra 1/4',
            'is_company': 'false'
        },

    ]
    update_datas = [
        {
            'name': 'Heiko Niemiec'
        },
    ]
    post_invalid_datas = [

    ]
    update_invalid_datas = [

    ]


class CompanyOrderInfoAPIViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'order_info/'
        init_test_db()
        self.api = TestAPI(token=get_token())
        self.view = CompanyOrderInfoAPIView.as_view()

    def test_get_data(self):
        valid_response = [
            {
                'Alternative Longboards': {
                    'Fantail': 61, 
                    'Erget': 14
                }
            },
            {
                'Bastl Boards': {
                    'Discofox': 40, 
                    'Bolero': 5}
            }
        ]

        request = self.api.get_request(self.endpoint)
        response = self.view(request)

        assert response.status_code == 200
        assert response.data == valid_response


class CompanyOrderInfoDetailAPIViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'order_info/'
        init_test_db()
        self.api = TestAPI(token=get_token())
        self.view = CompanyOrderInfoDetailAPIView.as_view()

    def test_get_data(self):
        valid_response = {
            "Fantail": 61,
            "Erget": 14
        }

        request = self.api.get_request(self.endpoint)
        response = self.view(request, 1)

        assert response.status_code == 200
        assert response.data == valid_response


class SendedBoardRecordAPIViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'add_sended_board/'
        init_test_db()
        self.api = TestAPI(token=get_token())
        self.view = SendedBoardRecordAPIView.as_view()

    def test_post_valid_board_to_valid_order(self):
        valid_message = { 
            "board": 188001000007,
            "order": 1
        }
        request = self.api.post_request(self.endpoint, valid_message)
        response = self.view(request)

        assert response.status_code == 201

    def test_post_invalid_board_to_valid_order(self):
        message = { 
            "board": 188001000008,
            "order": 1
        }
        request = self.api.post_request(self.endpoint, message)
        response = self.view(request)

        assert response.status_code == 400

    def test_post_invalid_board_to_invalid_order(self):
        message = { 
            "board": 111,
            "order": 66
        }
        request = self.api.post_request(self.endpoint, message)
        response = self.view(request)

        assert response.status_code == 400

    def test_post_sended_board_to_valid_order(self):
        message = {
            "board": 188001000010,
            "order": 1
        }
        request = self.api.post_request(self.endpoint, message)
        response = self.view(request)

        assert response.status_code == 400

    def test_post_sended_board_to_invalid_order(self):
        message = {
            "board": 188001000020,
            "order": 3
        }
        request = self.api.post_request(self.endpoint, message)
        response = self.view(request)

        assert response.status_code == 400

    def test_delete_valid_board_from_valid_order(self):
        message = {
            "board": 188001000010,
            "order": 1
        }
        request = self.api.delete_request(self.endpoint, message)
        response = self.view(request, board=message['board'])

        assert response.status_code == 200

    def test_delete_invalid_board_from_valid_order(self):
        message = {
            "board": 1111,
            "order": 1
        }
        request = self.api.delete_request(self.endpoint, message)
        response = self.view(request, board=message['board'])

        assert response.status_code == 400

    def test_delete_invalid_board_from_invalid_order(self):
        message = {
            "board": 1111,
            "order": 66
        }
        request = self.api.delete_request(self.endpoint, message)
        response = self.view(request, board=message['board'])

        assert response.status_code == 400
