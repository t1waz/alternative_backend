from django.test import TestCase
from unittest.mock import MagicMock
from .auth import BaseAccess, ACCESS_KEY


class AuthTestTestCases(TestCase):
	def setUp(self):
		self.permission = BaseAccess()

	def test_base_access_with_valid_token(self):
		request = MagicMock()
		request.META = {"HTTP_ACCESS_TOKEN": ACCESS_KEY}

		assert self.permission.has_permission(request, view=MagicMock())

	def test_base_access_with_not_valid_token(self):
		request = MagicMock()
		request.META = {"HTTP_ACCESS_TOKEN": "NOT LEGIT ACCESS TOKEN"}

		assert not self.permission.has_permission(request, view=MagicMock())
