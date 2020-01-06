from common import constants
from django.core.management import call_command
from rest_framework.test import APIRequestFactory


def seconds_between_timestamps(start_timestamp, finish_timestamp):
    return (finish_timestamp - start_timestamp).total_seconds()


def init_test_db():
    call_command('loaddata', 'seed_db.json', verbosity=1)


def get_token():
    from workers.views import WorkerLoginAPIView
    view = WorkerLoginAPIView.as_view()
    data = {
        "username": "Szymon Smialek",
        "password": "bbb"
    }
    request = APIRequestFactory().post('login/', data, **constants.HEADERS)
    response = view(request)

    return response.data['token']
