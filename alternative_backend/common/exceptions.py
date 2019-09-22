from rest_framework.exceptions import APIException


class ServiceException(Exception):
    pass


class CustomException(APIException):
    status_code = None
    info = None

    def __init__(self, status_code, info):
        CustomException.status_code = info
        CustomException.info = info
