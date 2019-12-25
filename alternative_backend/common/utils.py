import json
from copy import deepcopy
from django.http import JsonResponse
from django.core.management import call_command
from rest_framework.test import APIRequestFactory
from common.middlewares import IdentyProviderMiddleware


HEADERS = {
    'CONTENT_TYPE': 'application/json',
    'format': 'json'
}

DETAIL_VIEW_ACTIONS = {
    'get': 'retrieve'
}

VIEW_ACTIONS = {
    'get': 'list',
    'post': 'create',
    'delete': 'destroy',
    'patch': 'partial_update'
}


def init_test_db():
    call_command('loaddata', 'seed_db.json', verbosity=1)


def get_token():
    from workers.views import WorkerLoginAPIView
    view = WorkerLoginAPIView.as_view()
    data = {
        "username": "Szymon Smialek",
        "password": "bbb"
    }
    request = APIRequestFactory().post('login/', data, **HEADERS)
    response = view(request)

    return response.data['token']


class TestAPI:
    def __init__(self, token):
        self.factory = APIRequestFactory()
        self.headers = deepcopy(HEADERS)
        self.headers['HTTP_ACCESS_TOKEN'] = token
        self.identy_provider = IdentyProviderMiddleware()

    def get_request(self, endpoint):
        response = self.factory.get('{}'.format(endpoint), **self.headers)
        self.identy_provider(response)

        return response

    def post_request(self, endpoint, data):
        response = self.factory.post('{}'.format(endpoint), data, **self.headers)
        self.identy_provider(response)

        return response

    def delete_request(self, endpoint, data=None):
        if not data:
            response = self.factory.delete('{}'.format(endpoint), **self.headers)
        else:
            response = self.factory.delete('{}'.format(endpoint), data, **self.headers)
        self.identy_provider(response)

        return response

    def patch_request(self, endpoint, data):
        response = self.factory.patch('{}'.format(endpoint), data, **self.headers)
        self.identy_provider(response)

        return response


class ViewSetTestsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.detail_view = self.view.as_view(actions=DETAIL_VIEW_ACTIONS)
        self.view = self.view.as_view(actions=VIEW_ACTIONS)
        if not hasattr(self, 'detail_serializer'):
            self.detail_serializer = self.serializer

    @classmethod
    def setUpTestData(cls):
        init_test_db()
        cls.api = TestAPI(token=get_token())
        cls.endpoint = getattr(cls, 'endpoint')
        cls.pk_key = getattr(cls, 'key_search', {'pk': '1'})

    def test_get_list(self):
        db_data = self.serializer(self.model.objects.all(), many=True)
        request = self.api.get_request(self.endpoint)
        response = self.view(request)
        request_raw_data = JsonResponse(response.data, safe=False)
        request_data = json.loads(request_raw_data.content)

        assert request_data == db_data.data

    def test_get_detail(self):      
        db_company = self.detail_serializer(self.model.objects.get(**self.pk_key))
        request = self.api.get_request(self.endpoint)
        response = self.detail_view(request, **self.pk_key)
        request_raw_data = JsonResponse(response.data, safe=False)
        request_data = json.loads(request_raw_data.content)

        assert request_data == db_company.data

    def test_post(self):
        for post_data in self.post_datas:
            request = self.api.post_request(self.endpoint, post_data)
            response = self.view(request)

            assert response.status_code == 201

    def test_post_invalid(self):
        for invalid_data in self.post_invalid_datas:
            request = self.api.post_request(self.endpoint, invalid_data)
            response = self.view(request)
            assert response.status_code != 201

    def test_update(self):
        for update_data in self.update_datas:
            request = self.api.patch_request(self.endpoint, update_data)
            response = self.view(request, **self.pk_key)

            assert response.status_code == 200

    def test_update_invalid(self):
        for invalid_data in self.update_invalid_datas:
            pk = invalid_data['pk']
            request = self.api.patch_request(self.endpoint, invalid_data)
            response = self.view(request, pk=pk)

            assert response.status_code != 201

    def test_delete(self):
        request = self.api.delete_request(self.endpoint)
        response = self.view(request, **self.pk_key)

        assert response.status_code == 204
