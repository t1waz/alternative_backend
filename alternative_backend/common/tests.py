import json
from django.http import JsonResponse
from django.test import TestCase
from unittest.mock import MagicMock
from django.core import serializers
from django.conf import settings
from .auth import BaseAccess
from django.core.management import call_command
from rest_framework.test import APIRequestFactory


def init_test_db():
    call_command('loaddata', 'seed_db.json', verbosity=0)


class TestAPI:
    def __init__(self):
        self.factory = APIRequestFactory()
        self.headers = {
            'HTTP_ACCESS_TOKEN': settings.ACCESS_KEY,
            'CONTENT_TYPE': 'application/json',
            'format': 'json'
        }

    def get_request(self, endpoint):
        return self.factory.get('{}'.format(endpoint), **self.headers)

    def post_request(self, endpoint, data):
        return self.factory.post('{}'.format(endpoint), data, **self.headers)

    def delete_request(self, endpoint, data=None):
        if not data:
            return self.factory.delete('{}'.format(endpoint), **self.headers)
        else:
            return self.factory.delete('{}'.format(endpoint), data, **self.headers)

    def patch_request(self, endpoint, data):
        return self.factory.patch('{}'.format(endpoint), data, **self.headers)


class ViewSetBaseTests:
    def __init__(self, *args, **kwargs):
        super(ViewSetBaseTests, self).__init__(*args, **kwargs)
        init_test_db()
        self.api = TestAPI()
        self.pk_key = 1
        self.view_actions = {'get': 'retrieve'}
        self.detail_view_actions = {'get': 'list',
                                    'post': 'create',
                                    'delete': 'destroy',
                                    'patch': 'partial_update'}

    def test_get_list(self):
        db_data = self.serializer(self.model.objects.all(), many=True)
        request = self.api.get_request(self.endpoint)
        response = self.view(request)
        request_raw_data = JsonResponse(response.data, safe=False)
        request_data = json.loads(request_raw_data.content)

        assert request_data == db_data.data

    def test_get_detail(self):
        db_company = self.serializer(self.model.objects.get(pk=self.pk_key))
        request = self.api.get_request(self.endpoint)
        response = self.detail_view(request, pk=self.pk_key)
        request_raw_data = JsonResponse(response.data, safe=False)
        request_data = json.loads(request_raw_data.content)

        assert request_data == db_company.data

    def test_post(self):
        request = self.api.post_request(self.endpoint, self.new_data)
        response = self.view(request)
        print(response.data)

        assert response.status_code == 201

    def test_delete(self):
        request = self.api.delete_request(self.endpoint)
        response = self.view(request, pk=self.pk_key)

        assert response.status_code == 204

    def test_update(self):
        for update_data in self.update_datas:
            request = self.api.patch_request(self.endpoint, update_data)
            response = self.view(request, pk=self.pk_key)
            updated_key = [key for key in update_data.keys()][0]
            print(response.data)
            assert response.data[updated_key] == update_data[updated_key]


class AuthTestTestCases(TestCase):
    def setUp(self):
        self.permission = BaseAccess()

    def test_base_access_with_valid_token(self):
        request = MagicMock()
        request.META = {"HTTP_ACCESS_TOKEN": settings.ACCESS_KEY}

        assert self.permission.has_permission(request, view=MagicMock())

    def test_base_access_with_not_valid_token(self):
        request = MagicMock()
        request.META = {"HTTP_ACCESS_TOKEN": "NOT LEGIT ACCESS TOKEN"}

        assert not self.permission.has_permission(request, view=MagicMock())
