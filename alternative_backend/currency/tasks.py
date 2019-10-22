from celery import shared_task
from currency.services import PriceService
from celery.signals import celeryd_after_setup


@shared_task
def get_currency_prices():
    PriceService().update_prices()


@celeryd_after_setup.connect
def get_currency_prices_on_startup(sender=None, conf=None, **kwargs):
    PriceService().update_prices()
