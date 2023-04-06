import requests
import json
from config import keys

class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod  # Метод для конвертации валюты
    def get_price(quote, base, amount):  # Переводим введенные данные в строки

        # Проверяем, что введенные валюты существуют
        if quote == base:  # Если обе валюты одинаковы
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        # Проверка, имеется ли введенная валюта в списке?
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Неправильно указана валюта {quote}. /values')

        # Проверка, имеется ли введенная валюта в списке?
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Неправильно указана валюта {base}. /values')

        # Проверяем, что введенное число является числом
        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f'Не удалось обработать количество валюты {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        price = total_base * amount

        return price
