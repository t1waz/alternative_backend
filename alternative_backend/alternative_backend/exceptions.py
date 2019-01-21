from rest_framework import exceptions


class AppException(exceptions.APIException):
    status_code = 400
    default_detail = "Service unavailable."
