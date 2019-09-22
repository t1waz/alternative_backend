import copy
import json
from django.http import JsonResponse
from django.test import TestCase
from workers.models import Worker
from stations.models import Station
from django.conf import settings
from common.tests import (
    ViewSetBaseTests,
    init_test_db,
    TestAPI,
)
from .models import (
    Board,
    BoardModel,
    BoardCompany,
    BoardScan,
)
from .views import (
    StockAPIView,
    BoardScanAPIView,
    BoardModelViewSet,
    ProductionAPIView,
    StockDetailAPIView,
    BoardCompanyViewSet,
    ProductionDetailAPIView,
    BoardViewSet,
)
from .serializers import (
    BoardModelSerializer,
    BoardCompanySerializer,
    BoardListSerializer,
    BoardDetailViewSerializer,
)


class BoardCompanyViewTests(ViewSetBaseTests, TestCase):
    def setUp(self):
        self.endpoint = 'companies/'
        self.serializer = BoardCompanySerializer
        self.model = BoardCompany
        self.new_data = {'name': 'Loaded',
                         'code': 30,
                         'description': 'one of the most popular companies'}
        self.update_datas = [{'description': 'new description'}]
        self.detail_view = BoardCompanyViewSet.as_view(actions=self.view_actions)
        self.view = BoardCompanyViewSet.as_view(actions=self.detail_view_actions)


class BoardModelViewTests(ViewSetBaseTests, TestCase):
    def setUp(self):
        self.endpoint = 'board_models/'
        self.serializer = BoardModelSerializer
        self.model = BoardModel
        self.new_data = {'name': 'Erget',
                         'description': 'one of the most popular boards',
                         'year': 2018,
                         'code': 30,
                         'company': self.model.objects.get(id=1).id}
        self.update_datas = [{'description': 'new description'}]
        self.detail_view = BoardModelViewSet.as_view(actions=self.view_actions)
        self.view = BoardModelViewSet.as_view(actions=self.detail_view_actions)


class BoardViewSetTests(ViewSetBaseTests, TestCase):
    def setUp(self):
        self.endpoint = 'boards'
        self.model = Board
        self.detail_view = BoardViewSet.as_view(actions={'get': 'retrieve',
                                                         'patch': 'partial_update'})
        self.view = BoardViewSet.as_view(actions={'get': 'list',
                                                  'post': 'create'})

    def test_get_list(self):
        db_data = BoardListSerializer(self.model.objects.all(), many=True)
        request = self.api.get_request(self.endpoint)
        response = self.view(request)
        request_raw_data = JsonResponse(response.data, safe=False)
        request_data = json.loads(request_raw_data.content)

        assert request_data == db_data.data

    def test_get_detail(self):
        db_company = BoardDetailViewSerializer(self.model.objects.get(barcode=181002000001))
        request = self.api.get_request(self.endpoint)
        response = self.detail_view(request, barcode=181002000001)
        request_raw_data = JsonResponse(response.data, safe=False)
        request_data = json.loads(request_raw_data.content)

        assert request_data == db_company.data

    def test_post(self):
        new_data = {'barcode': 181002123456}
        request = self.api.post_request(self.endpoint, new_data)
        response = self.view(request)

        assert response.status_code == 201

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
        wrong_barcodes = [int(''.join(['1' for _ in range(settings.BARCODE_LENGHT + 1)])),
                          int(''.join(['1' for _ in range(settings.BARCODE_LENGHT - 1)])),
                          int(str(191010) + ''.join(['1' for _ in range(settings.BARCODE_LENGHT - 5)])),
                          int(str(191010) + ''.join(['1' for _ in range(settings.BARCODE_LENGHT - 7)])),
                          int(str(199910) + ''.join(['1' for _ in range(settings.BARCODE_LENGHT - 5)])),
                          int(str(191099) + ''.join(['1' for _ in range(settings.BARCODE_LENGHT - 7)]))]
        for wrong_barcode in wrong_barcodes:
            wrong_message = {'barcode': wrong_barcode}
            request = self.api.post_request(self.endpoint, wrong_message)
            response = self.view(request)

            assert response.status_code == 400

    def test_delete(self):
        pass

    def test_update(self):
        valid_message = {'barcode': 181002000001,
                         'second_category': True}
        request = self.api.patch_request(self.endpoint, valid_message)
        response = self.detail_view(request, barcode=valid_message['barcode'])

        assert response.status_code == 200

        valid_message_2 = copy.copy(valid_message)
        valid_message_2['second_category'] = False

        request = self.api.patch_request(self.endpoint, valid_message)
        response = self.detail_view(request, barcode=valid_message['barcode'])

        assert response.status_code == 200

    def test_non_existing_barcode(self):
        wrong_message = {'barcode': 199910654321,
                         'second_category': True}

        request = self.api.patch_request(self.endpoint, wrong_message)
        response = self.detail_view(request, barcode=wrong_message['barcode'])

        assert response.status_code == 404


class BoardScanAPIViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'add_scan/'
        init_test_db()
        self.api = TestAPI()
        self.worker = Worker.objects.get(barcode=111111111111)
        self.barcode = Board.objects.get(id=3)
        self.view = BoardScanAPIView.as_view()
        self.valid_message = {"barcode": self.barcode.barcode,
                              "worker": self.worker.username,
                              "station": Station.objects.get(id=2).name}

    def test_valid_data(self):
        request = self.api.post_request(self.endpoint, self.valid_message)
        response = self.view(request)

        assert response.status_code == 201

    def test_adding_missing_scans(self):
        message = copy.copy(self.valid_message)
        message['station'] = Station.objects.get(id=3).name
        request = self.api.post_request(self.endpoint, message)
        response = self.view(request)

        assert response.status_code == 201

        is_missing_scan = BoardScan.objects.filter(barcode=self.barcode,
                                                   worker=self.worker,
                                                   station=Station.objects.get(id=2)).exists()

        assert is_missing_scan is True    

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


class ProductionAPIViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'production/'
        init_test_db()
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
        self.endpoint = 'production/'
        init_test_db()
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
        init_test_db()
        self.api = TestAPI()
        self.view = StockAPIView.as_view()

    def test_get_data(self):
        valid_response = {
            'Alternative Longboards': {
                'Fantail': 1,
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
        init_test_db()
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
