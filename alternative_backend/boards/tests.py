import json
import copy
from django.test import TestCase
from workers.models import Worker
from common.auth import ACCESS_KEY
from django.core import serializers
from stations.models import Station
from rest_framework.test import APIRequestFactory
from alternative_backend.settings import BARCODE_LENGHT
from .models import (
    Board,
    BoardModel,
    BoardCompany,
)
from .views import (
    StockAPIView,
    BoardScanAPIView,
    BoardModelViewSet,
    ProductionAPIView,
    StockDetailAPIView,
    BarcodeInfoAPIView,
    BoardCompanyViewSet,
    NewBoardBarcodeAPIView,
    ProductionDetailAPIView,
    BarcodeInfoDetailAPIView,
    BoardSecondCategoryAPIView,
)
from .serializers import (
    BoardModelSerializer,
    BoardCompanySerializer,
    BoardPresentationSerializer,
)


def init_db():
    f = open("seed_db.json", "r")
    for deserialized_object in serializers.deserialize("json", f):
        deserialized_object.save()


class TestAPI:
    def __init__(self):
        self.factory = APIRequestFactory()

    def get_request(self, endpoint):
        return self.factory.get('{}'.format(endpoint),
                                HTTP_ACCESS_TOKEN=ACCESS_KEY, CONTENT_TYPE='application/json')

    def post_request(self, endpoint, data):
        return self.factory.post('{}'.format(endpoint), data,
                                 HTTP_ACCESS_TOKEN=ACCESS_KEY, CONTENT_TYPE='application/json')

    def delete_request(self, endpoint):
        return self.factory.delete('{}'.format(endpoint),
                                   HTTP_ACCESS_TOKEN=ACCESS_KEY, CONTENT_TYPE='application/json')

    def patch_request(self, endpoint, data):
        return self.factory.patch('{}'.format(endpoint), data,
                                  HTTP_ACCESS_TOKEN=ACCESS_KEY, CONTENT_TYPE='application/json')


class BoardCompanyViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'companies/'
        init_db()
        self.api = TestAPI()
        self.detail_view = BoardCompanyViewSet.as_view(actions={'get': 'retrieve'})
        self.view = BoardCompanyViewSet.as_view(actions={'get': 'list',
                                                         'post': 'create',
                                                         'delete': 'destroy',
                                                         'patch': 'partial_update'})

    def test_get_list(self):
        db_data = BoardCompanySerializer(BoardCompany.objects.all(), many=True)
        request = self.api.get_request(self.endpoint)
        response = self.view(request)
        request_data = json.loads(json.dumps(response.data))

        assert request_data == db_data.data

    def test_get_detail(self):
        db_company = BoardCompanySerializer(BoardCompany.objects.get(id=1))
        request = self.api.get_request(self.endpoint)
        response = self.detail_view(request, pk=1)
        request_data = json.loads(json.dumps(response.data))

        assert request_data == db_company.data

    def test_post(self):
        new_company = {'name': 'Loaded',
                       'code': 30,
                       'description': 'one of the most popular companies'}
        request = self.api.post_request(self.endpoint, new_company)
        response = self.view(request)

        assert response.status_code == 201

    def test_delete(self):
        request = self.api.delete_request(self.endpoint)
        response = self.view(request, pk=1)

        assert response.status_code == 204

    def test_update(self):
        new_data = {'description': 'new description'}
        request = self.api.patch_request(self.endpoint, new_data)
        response = self.view(request, pk=1)

        assert response.data['description'] == new_data['description']


class BoardModelViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'board_models/'
        init_db()
        self.api = TestAPI()
        self.detail_view = BoardModelViewSet.as_view(actions={'get': 'retrieve'})
        self.view = BoardModelViewSet.as_view(actions={'get': 'list',
                                                       'post': 'create',
                                                       'delete': 'destroy',
                                                       'patch': 'partial_update'})

    def test_get_list(self):
        db_data = BoardModelSerializer(BoardModel.objects.all(), many=True)
        request = self.api.get_request(self.endpoint)
        response = self.view(request)
        request_data = json.loads(json.dumps(response.data))

        assert request_data == db_data.data

    def test_get_detail(self):
        db_company = BoardModelSerializer(BoardModel.objects.get(id=1))
        request = self.api.get_request(self.endpoint)
        response = self.detail_view(request, pk=1)
        request_data = json.loads(json.dumps(response.data))

        assert request_data == db_company.data

    def test_post(self):
        new_board_model = {'name': 'Erget',
                           'description': 'one of the most popular boards',
                           'year': 2018,
                           'code': 30,
                           'company': BoardCompany.objects.get(id=1).id}
        request = self.api.post_request(self.endpoint, new_board_model)
        response = self.view(request)

        assert response.status_code == 201

    def test_delete(self):
        request = self.api.delete_request(self.endpoint)
        response = self.view(request, pk=1)

        assert response.status_code == 204

    def test_update(self):
        new_data = {'description': 'new description'}
        request = self.api.patch_request(self.endpoint, new_data)
        response = self.view(request, pk=1)

        assert response.data['description'] == new_data['description']


class BoardScanAPIViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'add_scan/'
        init_db()
        self.api = TestAPI()
        self.view = BoardScanAPIView.as_view()
        self.valid_message = {"barcode": Board.objects.get(id=3).barcode,
                              "worker": Worker.objects.get(barcode=111111111111).username,
                              "station": Station.objects.get(id=2).name}

    def test_valid_data(self):
        request = self.api.post_request(self.endpoint, self.valid_message)
        response = self.view(request)

        assert response.status_code == 200

    def test_wrong_barcode(self):
        wrong_barcodes = [111, 'aaa', '', 1.0]
        for wrong_barcode in wrong_barcodes:
            wrong_message = copy.copy(self.valid_message)
            wrong_message['barcode'] = wrong_barcode
            request = self.api.post_request(self.endpoint, wrong_message)
            response = self.view(request)

            assert response.status_code == 400

    def test_wrong_worker(self):
        wrong_workers = [111, 'Beju', '', 3.14]
        for wrong_worker in wrong_workers:
            wrong_message = copy.copy(self.valid_message)
            wrong_message['worker'] = wrong_worker
            request = self.api.post_request(self.endpoint, wrong_message)
            response = self.view(request)

            assert response.status_code == 400

    def test_wrong_station(self):
        wrong_stations = [111, 'non existing', 2.0]
        for wrong_station in wrong_stations:
            wrong_message = copy.copy(self.valid_message)
            wrong_message['station'] = wrong_station
            request = self.api.post_request(self.endpoint, wrong_message)
            response = self.view(request)

            assert response.status_code == 400

    def test_duplicated_scan(self):
        wrong_message = {"barcode": Board.objects.get(id=1).barcode,
                         "worker": Worker.objects.get(barcode=111111111111).username,
                         "station": Station.objects.get(id=1).name}
        request = self.api.post_request(self.endpoint, wrong_message)
        response = self.view(request)

        assert response.status_code == 400


class NewBoardBarcodeAPIViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'add_barcode'
        init_db()
        self.api = TestAPI()
        self.view = NewBoardBarcodeAPIView.as_view()
        self.valid_message = {'barcode': 181002123456}

    def test_valid_data(self):
        request = self.api.post_request(self.endpoint, self.valid_message)
        response = self.view(request)

        assert response.status_code == 200

    def test_wrong_model(self):
        wrong_message = {'barcode': 199910654321}
        request = self.api.post_request(self.endpoint, wrong_message)
        response = self.view(request)

        assert response.status_code == 400

    def test_wrong_company(self):
        wrong_message = {'barcode': 191099654321}
        request = self.api.post_request(self.endpoint, wrong_message)
        response = self.view(request)

        assert response.status_code == 400

    def test_wrong_barcode_lenght(self):
        wrong_barcodes = [int(''.join(['1' for _ in range(BARCODE_LENGHT + 1)])),
                          int(''.join(['1' for _ in range(BARCODE_LENGHT - 1)])),
                          int(str(191010) + ''.join(['1' for _ in range(BARCODE_LENGHT - 5)])),
                          int(str(191010) + ''.join(['1' for _ in range(BARCODE_LENGHT - 7)])),
                          int(str(199910) + ''.join(['1' for _ in range(BARCODE_LENGHT - 5)])),
                          int(str(191099) + ''.join(['1' for _ in range(BARCODE_LENGHT - 7)]))]
        for wrong_barcode in wrong_barcodes:
            wrong_message = {'barcode': wrong_barcode}
            request = self.api.post_request(self.endpoint, wrong_message)
            response = self.view(request)

            assert response.status_code == 400


class BoardSecondCategoryAPIViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'add_second_category/'
        init_db()
        self.api = TestAPI()
        self.view = BoardSecondCategoryAPIView.as_view()
        self.valid_message = {'barcode': 181002000001,
                              'second_category': True}

    def test_valid_data(self):
        request = self.api.post_request(self.endpoint, self.valid_message)
        response = self.view(request)

        assert response.status_code == 200

        valid_message_2 = copy.copy(self.valid_message)
        valid_message_2['second_category'] = False

        request = self.api.post_request(self.endpoint, valid_message_2)
        response = self.view(request)

        assert response.status_code == 200

    def test_non_existing_barcode(self):
        wrong_message = copy.copy(self.valid_message)
        wrong_message['barcode'] = 199910654321
        request = self.api.post_request(self.endpoint, wrong_message)
        response = self.view(request)

        assert response.status_code == 400


class ProductionAPIViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'production/'
        init_db()
        self.api = TestAPI()
        self.view = ProductionAPIView.as_view()

    def test_get_data(self):
        valid_response = {
            "Alternative Longboards": {
                "PRESS": {
                    "Erget": 1,
                    "Fantail": 1},
                "CUT": {
                    "Fantail": 1,
                    "Erget": 0}},
            "Bastl Boards": {
                "PRESS": {
                    "Discofox": 0,
                    "Bolero": 0},
                "CUT": {
                    "Bolero": 1,
                    "Discofox": 0}
            }
        }
        request = self.api.get_request(self.endpoint)
        response = self.view(request)

        assert response.status_code == 200
        assert response.data == valid_response


class ProductionDetailAPIViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'production'
        init_db()
        self.api = TestAPI()
        self.view = ProductionDetailAPIView.as_view()

    def test_get_data(self):
        valid_response = {
            'PRESS': {
                'Erget': 1, 
                'Fantail': 1}, 
            'CUT': {
                'Fantail': 1, 
                'Erget': 0}
        }
        request = self.api.get_request(self.endpoint)
        response = self.view(request, 1)

        assert response.status_code == 200 
        assert response.data == valid_response


class StockAPIViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'stock/'
        init_db()
        self.api = TestAPI()
        self.view = StockAPIView.as_view()

    def test_get_data(self):
        valid_response = {
            'Alternative Longboards': {
                'Fantail': 0, 
                'Erget': 0}, 
            'Bastl Boards': {
                'Discofox': 1, 
                'Bolero': 0}
        }
        request = self.api.get_request(self.endpoint)
        response = self.view(request)

        assert response.status_code == 200
        assert response.data == valid_response


class StockDetailAPIViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'stock/'
        init_db()
        self.api = TestAPI()
        self.view = StockDetailAPIView.as_view()

    def test_get_data(self):
        valid_response = {
            'Discofox': 1, 
            'Bolero': 0
        }
        request = self.api.get_request(self.endpoint)
        response = self.view(request, 2)

        assert response.status_code == 200
        assert response.data == valid_response


class BarcodeInfoAPIViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'boards/'
        init_db()
        self.api = TestAPI()
        self.view = BarcodeInfoAPIView.as_view()

    def test_get_data(self):
        boards = Board.objects.all()
        valid_response = BoardPresentationSerializer(boards, many=True).data
        request = self.api.get_request(self.endpoint)
        response = self.view(request)

        assert response.status_code == 200
        assert response.data == valid_response


class BarcodeInfoDetailAPIViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'boards/'
        init_db()
        self.api = TestAPI()
        self.view = BarcodeInfoDetailAPIView.as_view()

    def test_get_data(self):
        board = Board.objects.get(barcode=181002000001)
        valid_response = BoardPresentationSerializer(board).data
        request = self.api.get_request(self.endpoint)
        response = self.view(request, 181002000001)

        assert response.status_code == 200
        assert response.data == valid_response
