from common.auth import BaseAccess
from django.test import TestCase
from unittest.mock import MagicMock
from common.utils import (
    init_test_db,
    get_token,
)


class AuthTestTestCases(TestCase):
    @classmethod
    def setUpTestData(cls):
        init_test_db()
        cls.token = get_token()
        cls.permission = BaseAccess()

    def test_base_access_with_valid_token(self):
        request = MagicMock()
        request.META = {"HTTP_ACCESS_TOKEN": self.token}

        assert self.permission.has_permission(request, view=MagicMock())

    def test_base_access_with_not_valid_token(self):
        request = MagicMock()
        request.META = {"HTTP_ACCESS_TOKEN": "NOT LEGIT ACCESS TOKEN"}

        assert not self.permission.has_permission(request, view=MagicMock())
