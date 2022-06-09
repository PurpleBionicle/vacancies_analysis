import requests
from parse.business_logic import Keys


class values():
    def __init__(self, value_usd, value_eur):
        self.usd = value_usd
        self.eur = value_eur


def get_course(currency, to_currency):
    global rate
    # print("Валюты вводятся по английски заглавными буквами")
    # print("Пример: USD , EUR , RUB ")
    #
    # base = input("Курс относительно какой валюты:")
    # other = input("Курс  какой валюты:")
    API_key = Keys.course

    response_base = requests.get(
        f"http://data.fixer.io/api/latest?access_key={API_key}&base=EUR&symbols={currency}")

    base_json = response_base.json()

    if to_currency != 'EUR':
        response_other = requests.get(
            f"http://data.fixer.io/api/latest?access_key={API_key}&base=EUR&symbols={to_currency}")

        if response_base.status_code != 200 or response_other.status_code != 200:
            raise Exception("ERROR invalid request")

        other_json = response_other.json()

        if base_json['success'] and other_json['success']:
            rate_b = base_json["rates"][str(currency)]
            rate_o = other_json["rates"][str(to_currency)]
            # API - только по евро работает -> надо найти отношение относительно евро
            rate = round((rate_o / rate_b), 2)

    else:
        rate = base_json["rates"][str(currency)]

    print(f"1 {currency} = {rate} {to_currency}")
    return rate


def course_transfer(value):
    # предполагаем ,что в рублях
    value_usd = value / get_course('USD', 'RUB')
    value_euro = value / get_course('EUR', 'RUB')
    result = values(value_usd, value_euro)
    return result , get_course('USD', 'RUB') , get_course('EUR', 'RUB')


if __name__ == '__main__':
    print(course_transfer(100))
