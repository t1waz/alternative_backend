from django.test import (
    TestCase,
    override_settings,
)

from boards.views import BoardViewSet
from common.constants import VIEW_ACTIONS
from common.utils import (
    ViewSetTestsMixin,
    init_test_db,
    get_token,
    TestAPI,
)
from workers.models import Worker
from workers.serializers import WorkerSerializer
from workers.views import (
    WorkerViewSet,
    WorkerLogoutAPIView,
    WorkerWorkHistoryAPIView,
)


@override_settings(MAX_NUMBER_OF_TOKENS=10000)
class WorkerViewSetTests(ViewSetTestsMixin, TestCase):
    model = Worker
    endpoint = 'workers/'
    view = WorkerViewSet
    serializer = WorkerSerializer
    key_search = {'pk': '111111111111'}
    post_datas = [
        {
            'username': 'Justa', 
            'barcode': 111111112222
        },
    ]
    update_datas = [
        {
            'username': 'Justa two'
        },
    ]
    post_invalid_datas = [

    ]
    update_invalid_datas = [

    ]


@override_settings(MAX_NUMBER_OF_TOKENS=10000)
class WorkerWorkHistoryAPIViewTests(TestCase):
    def setUp(self):
        self.endpoint = 'add_worker_scan/'
        init_test_db()
        self.api = TestAPI(token=get_token())
        self.view = WorkerWorkHistoryAPIView.as_view()

    def test_post_valid_worker_scan(self):
        valid_worker_scan = {'worker': 111111111111}
        request = self.api.post_request(self.endpoint, valid_worker_scan)
        response = self.view(request)

        assert response.status_code == 200

    def test_post_invalid_worker(self):
        invalid_worker_barcodes = [111111111112, 11111111111, 'aaa', 3.14]
        invalid_worker_scan = {'worker': 111111111111}
        invalid_names = [11, 'aa', 3.13]

        for invalid_barcode in invalid_worker_barcodes:
            invalid_worker_scan['worker'] = invalid_barcode
            request = self.api.post_request(self.endpoint, invalid_worker_scan)
            response = self.view(request)

            assert response.status_code == 400

        for invalid_barcode in invalid_worker_barcodes:
            invalid_worker_scan['worker'] = invalid_barcode
            invalid_worker_scan['aa'] = invalid_barcode
            request = self.api.post_request(self.endpoint, invalid_worker_scan)
            response = self.view(request)

            assert response.status_code == 400

        for invalid_name in invalid_names:
            invalid_worker_scan[invalid_name] = 111111111111
            request = self.api.post_request(self.endpoint, invalid_worker_scan)
            response = self.view(request)

            assert response.status_code == 400


@override_settings(MAX_NUMBER_OF_TOKENS=10000)
class LogoutTestCase(TestCase):
    def setUp(self):
        self.endpoint = 'logout/'
        init_test_db()
        self.api = TestAPI(token=get_token())
        self.view = WorkerLogoutAPIView.as_view()

    def test_logout_user(self):
        boards_view = BoardViewSet.as_view(actions=VIEW_ACTIONS)
        request = self.api.get_request('boards/')
        response = boards_view(request)

        assert response.status_code == 200

        request = self.api.get_request(self.endpoint)
        response = self.view(request)

        request = self.api.get_request('boards/')
        response = boards_view(request)

        assert response.status_code != 200
