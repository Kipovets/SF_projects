import requests
import json
from config import keys

class APIExeption(Exception):
    pass


# Выбранный API предоставляет данные в виде словаря с вложенным словарем {пара_валют : конвертированная стоимость},
# поэтому функция предусматривает получение значений словаря в виде списка, после чего мы по ключу "пара_валют"
# получаем конвертированную стоимость
class CurrencyConverter:
    @staticmethod
    def get_price(quote:str, base:str, amount:str):
        try:
            tr_quote = keys[quote]
            tr_base = keys[base]
        except KeyError:
            raise APIExeption("Неверно введена валюта (может быть она мне просто пока незнакома 🤨)")

        try:
            amount = float(amount)
        except ValueError:
            raise APIExeption("Количество валюты измеряется циферками! Вы ошиблись ☹")

        if quote == base:
            raise APIExeption("Валюту нельзя перевести саму в себя! Давайте что-нибудь изменим!")

        r = requests.get(f"https://currate.ru/api/?get=rates&pairs={tr_quote}{tr_base}&key=e1d8a7efd8f9664b7b91267a0b13d281")
        t = list(json.loads(r.content).values())[2]
        total_base = float(t[f"{tr_quote}{tr_base}"]) * amount
        return total_base