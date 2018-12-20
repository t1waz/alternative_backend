from rest_framework import permissions

ACCESS_KEY = "123dupachujpietaszekalternativelongboards"

class BaseAccess(permissions.BasePermission):
	"""
	Checks if request got valid access key
	"""
	def has_permission(self, request, view):
		request_token = request.META['HTTP_ACCESS_TOKEN']
		return request_token == ACCESS_KEY

