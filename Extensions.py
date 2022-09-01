import json
import requests
from config import values

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(amount: str, quote: str, base: str):

        if quote == base:
            raise APIException (f'Транзакция невозможна, валюты совпадают {quote}')
        try:
            quote_ticker = values[quote]
        except KeyError:
            raise APIException(f'не удалось обработать заявку на валюту {quote}')
        try:
            base_ticker = values[base]
        except KeyError:
            raise APIException(f'не удалось обработать заявку на валюту {base}')
        try:
            amount=float(amount)
        except ValueError:
            raise APIException(f'неправильно введено количество {amount}')

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total = float(json.loads(r.content)[values[base]])
        total *= amount
        return total
