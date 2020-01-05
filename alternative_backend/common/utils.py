import json
from copy import deepcopy
from common import constants
from django.http import JsonResponse
from rest_framework.test import APIRequestFactory
from django.core.exceptions import ValidationError
from common.helpers import (
    init_test_db,
    get_token,
)


class SimpleValidator:
    def set_context(self, serializer):
        self.fields = serializer.Meta.fields
        self.instance = getattr(serializer, 'instance', None)
        self.updated_fields = [field for field in dir(self) if field in self.fields]
        self.required_fields = getattr(serializer.Meta, 'required_fields', set())

    def run_validators(self, value):
        validators = getattr(self, 'validators')

        for validator in validators:
            try:
                validator(**value)
            except:  # TODO
                raise ValidationError('incorrect data for {}'.format(validator))  # TODO

    def __call__(self, value):
        common_fields = set(self.fields).intersection(set(self.updated_fields))
        common_fields = common_fields.union(self.required_fields)
        if not self.instance or common_fields:
            self.run_validators(value)


class TestAPI:
    def __init__(self, token):
        from common.middlewares import IdentyProviderMiddleware

        self.factory = APIRequestFactory()
        self.headers = deepcopy(constants.HEADERS)
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
        self.detail_view = self.view.as_view(actions=constants.DETAIL_VIEW_ACTIONS)
        self.view = self.view.as_view(actions=constants.VIEW_ACTIONS)
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
