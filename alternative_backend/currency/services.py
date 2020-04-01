import requests
from django.db import transaction

from common.exceptions import ServiceException
from currency.constans import (
    HEADERS,
    POLAND_SYMBOL,
)
from currency.models import Currency


class PriceService:
    @transaction.atomic
    def update_prices(self):
        all_currency = Currency.objects.all()

        for currency in all_currency:
            currency.price = self.download_price_for_symbol(symbol=currency.symbol)
            currency.save()

    def download_price_for_symbol(self, symbol):
        if symbol == POLAND_SYMBOL:
            return 1

        response = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/{}'.format(symbol),
                                headers=HEADERS)
        data = response.json()

        if response.status_code == 200:
            return data['rates'][0]['mid']
        else:
            raise ServiceException('cannot download price for '.format(symbol))
