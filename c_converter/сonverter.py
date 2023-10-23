import requests
from bs4 import BeautifulSoup

from currency_converter import CurrencyConverter

from c_converter.currencies import CURRENCIES_SYMBOLS_CODES_DICT

BASE_URL = r'https://www.google.com/finance/quote/'
HTML_CLASS_NAME = 'YMlKec fxKbKc'

EXCHANGE_RATE = {}
EXCHANGE_RATE_STATIC = {}

EXCHANGED_RATE_FIXED = {
    'USD': 1.0,
    'EUR': 1.05,
    'CNY': 0.15
}

currencies = tuple(c for c in CURRENCIES_SYMBOLS_CODES_DICT.values() if c != 'USD')


def set_exchange_rates():
    """
    Set base exchange rates from google finance.
    :return: None
    """
    for currency in currencies:
        add_url = fr'{currency}-USD'
        url = BASE_URL + add_url

        source = requests.get(url)
        main_text = source.text
        soup = BeautifulSoup(main_text)

        tag = soup.find('div', {'class': f'{HTML_CLASS_NAME}'})
        rate = tag.text

        EXCHANGE_RATE[currency] = rate


def set_exchange_rates_static():
    """
    Set additional exchange rates, if base exchange rates can not set.
    :return: None
    """
    c = CurrencyConverter()
    for currency in currencies:
        rate = c.convert(1, currency, 'USD')
        EXCHANGE_RATE_STATIC[currency] = rate


def set_rates():
    """
    Set all types of exchanges rates/
    :return: int
    """
    if not EXCHANGE_RATE:
        try:
            set_exchange_rates()
        except Exception:
            if not EXCHANGE_RATE_STATIC:
                try:
                    set_exchange_rates_static()
                except Exception:
                    return None
            return 2
    return 1


def get_rates():
    """
    Returns exchange rate.
    :return: dict
    """
    if not EXCHANGE_RATE and not EXCHANGE_RATE_STATIC:
        set_rates()
    if EXCHANGE_RATE:
        return EXCHANGE_RATE
    if EXCHANGE_RATE_STATIC:
        return EXCHANGE_RATE_STATIC
    return EXCHANGED_RATE_FIXED


def convert(currency: str, amount: float) -> float:
    """
    Converts the value of the selected currency into USD/
    :param currency: str
    :param amount: float
    :return: float
    """
    try:
        rate = float(EXCHANGE_RATE[currency])
    except Exception:
        try:
            rate = float(EXCHANGE_RATE_STATIC[currency])
        except Exception:
            rate = float(EXCHANGED_RATE_FIXED[currency])
    return rate * amount
