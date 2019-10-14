from django.test import TestCase
from workers.models import Worker
from workers.serializers import WorkerSerializer
from common.tests import (
    ViewSetBaseTests,
    TestAPI,
    init_test_db,
)
from workers.views import (
    WorkerViewSet,
    NewWorkerScanAPIView,
)


class WorkerViewSetTests(ViewSetBaseTests, TestCase):
    def setUp(self):
        self.endpoint = 'workers/'
        self.serializer = WorkerSerializer
        self.model = Worker
        self.pk_key = 111111111111
        self.new_data = {'username': 'Justa', 
                         'barcode': 111111112222}
        self.update_datas = [{'username': 'Justa two'}]
        self.detail_view = WorkerViewSet.as_view(actions=self.view_actions)
        self.view = WorkerViewSet.as_view(actions=self.detail_view_actions)


class NewWorkerScanAPIViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'add_worker_scan/'
        init_test_db()
        self.api = TestAPI()
        self.view = NewWorkerScanAPIView.as_view()

    def test_post_valid_worker_scan(self):
        valid_worker_scan = {'worker_barcode': 111111111111,
                             'started': True}
        request = self.api.post_request(self.endpoint, valid_worker_scan)
        response = self.view(request)

        assert response.status_code == 200

    def test_post_invalid_worker(self):
        invalid_worker_barcodes = [111111111112, 11111111111, 'aaa', 3.14]
        invalid_states = ['aaa', 11, None, 2.15]
        invalid_worker_scan = {'worker_barcode': 111111111111,
                               'started': True}
        for invalid_barcode in invalid_worker_barcodes:
            invalid_worker_scan['worker_barcode'] = invalid_barcode
            request = self.api.post_request(self.endpoint, invalid_worker_scan)
            response = self.view(request)

            assert response.status_code == 400

        for invalid_state in invalid_states:
            invalid_worker_scan['started'] = invalid_state
            request = self.api.post_request(self.endpoint, invalid_worker_scan)
            response = self.view(request)

            assert response.status_code == 400

        for invalid_worker_barcode in invalid_worker_barcodes:
            for invalid_state in invalid_states:
                invalid_worker_scan['worker_barcode'] = invalid_worker_barcode
                invalid_worker_scan['stated'] = invalid_state
                request = self.api.post_request(self.endpoint, invalid_worker_scan)
                response = self.view(request)

                assert response.status_code == 400
