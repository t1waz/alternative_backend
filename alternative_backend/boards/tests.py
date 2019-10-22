import copy
from django.test import TestCase
from workers.models import Worker
from stations.models import Station
from common.utils import (
    ViewSetTestsMixin,
    init_test_db,
    get_token,
    TestAPI,
)
from boards.models import (
    Board,
    BoardModel,
    BoardCompany,
    BoardScan,
)
from boards.views import (
    StockAPIView,
    BoardScanAPIView,
    BoardModelViewSet,
    ProductionAPIView,
    StockDetailAPIView,
    BoardCompanyViewSet,
    ProductionDetailAPIView,
    BoardViewSet,
)
from boards.serializers import (
    BoardModelSerializer,
    BoardCompanySerializer,
    BoardListSerializer,
    BoardDetailViewSerializer,
)


class BoardCompanyViewTests(ViewSetTestsMixin, TestCase):
    model = BoardCompany
    endpoint = 'companies/'
    view = BoardCompanyViewSet
    serializer = BoardCompanySerializer
    post_datas = [
        {
            'name': 'Loaded',
            'code': 30,
            'description': 'one of the most popular companies'
        },
    ]
    update_datas = [
        {
            'description': 'new description'
        },
    ]
    post_invalid_datas = [
        {
            'name': 'Loaded',
            'code': 100,
            'description': 'one of the most popular companies'
        },
        {
            'name': 'Loadedsdfsdfsdfsfdsdfasdddddddddddddddddddddddddddddddddddddddd\
            ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddasasdddd\
            dddddddddddddddddddddddddddddddddddddddd',
            'code': 1,
            'description': 'one of the most popular companies'
        },
        {
            'name': 'Loaded',
            'code': 1,
            'description': 'one of sdfffffffffffffffffffffffffffffffffffffffffffffff\
            ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\
            fffffffffffffffffffffffffffffffdsfthe mo'
        },
    ]
    update_invalid_datas = [

    ]


class BoardModelViewTests(ViewSetTestsMixin, TestCase):
    model = BoardModel
    endpoint = 'board_models/'
    view = BoardModelViewSet
    serializer = BoardModelSerializer
    post_datas = [
        {
            'name': 'Erget_2',
            'description': 'one of the most popular boards',
            'year': 2018,
            'code': 35,
            'company': 1
        },

    ]
    update_datas = [
        {
            'description': 'new description'
        },
    ]
    post_invalid_datas = [
        {
            'name': 'Erget',
            'description': 'one of the most popular boards',
            'year': 2018,
            'code': 35,
            'company': 1
        },
        {
            'name': 'Erget_3',
            'description': 'one of the most popular boards',
            'year': 20181,
            'code': 35,
            'company': 1
        },
        {
            'name': 'Erget_4',
            'description': 'one of the most popular boards',
            'year': 2018,
            'code': 351,
            'company': 1
        },
        {
            'name': 'Erget_5',
            'description': 'one of the most popular boards',
            'year': 2018,
            'code': 35,
            'company': 12
        },
        {
            'name': 'Erget_6',
            'description': 'one of thasddddddddddddddddddddddddddddddddddddddddddd\
            dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\
            ddddddddddddddddddddddddddddasdasdasdasdasda',
            'year': 2018,
            'code': 35,
            'company': 12
        },
        {
            'name': 'Erget',
            'description': 'one of thasdddddddddddddddddddddddddddddddddddddddddddd\
            ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\
            ddddddddddddddddddddddddddasdasdasdasdasda',
            'year': 2018123,
            'code': 351,
            'company': 124
        },

    ]
    update_invalid_datas = [

    ]


class BoardViewSetTests(ViewSetTestsMixin, TestCase):
    model = Board
    endpoint = 'boards/'
    view = BoardViewSet
    serializer = BoardListSerializer
    detail_serializer = BoardDetailViewSerializer
    key_search = {'barcode': 181002000001}
    post_datas = [
        {
            'barcode': 181002123456
        },
    ]
    update_datas = [
        {
            'barcode': 181002000001,
            'second_category': True
        },
        {
            'barcode': 181002000001,
            'second_category': False
        },
    ]
    post_invalid_datas = [
        {
            'barcode': 199910654321
        },
        {
            'barcode': 191099654321
        },
        {
            'barcode': 1910996543211
        },
        {
            'barcode': 19109965432
        },
        {
            'barcode': 19221099654321
        },
        {
            'barcode': 100099654321
        },
        {
            'barcode': 199910654321,
            'second_category': True
        },

    ]
    update_invalid_datas = [

    ]


class BoardScanAPIViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'add_scan/'
        init_test_db()
        self.api = TestAPI(token=get_token())
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
        self.api = TestAPI(token=get_token())
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
        self.api = TestAPI(token=get_token())
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
        self.api = TestAPI(token=get_token())
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
        self.api = TestAPI(token=get_token())
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
