from unittest.mock import MagicMock

from django.test import (
    TestCase,
    override_settings,
)

from common.auth import BaseAccess
from common.utils import (
    get_token,
    init_test_db,
)


@override_settings(MAX_NUMBER_OF_TOKENS=10000)
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
