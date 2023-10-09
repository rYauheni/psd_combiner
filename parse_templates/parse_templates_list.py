from parse_templates.parse_template import ParseTemplate
from сurrency_сonvertion.currencies import CURRENCIES_SYMBOLS

TEMPLATES_TITLES = {
    'buy_in': 'buy_in',
    'currency': 'currency',
    'total_received': 'total_received',
    're_entry': 're_entry'
}

PARSE_TEMPLATES = (
    ParseTemplate(
        title=f'{TEMPLATES_TITLES["buy_in"]}',
        detector=r'(?i)tournament #\d+',
        start=fr'[{CURRENCIES_SYMBOLS}]',
        end=r' ',
        required=True,
        ttype=float
    ),

    ParseTemplate(
        title=f'{TEMPLATES_TITLES["currency"]}',
        detector=fr'(?i)buy-in: [{CURRENCIES_SYMBOLS}]',
        start=r'(?i)buy-in: ',
        end=r'\d+',
        required=True,
        ttype=str
    ),

    ParseTemplate(
        title=f'{TEMPLATES_TITLES["total_received"]}',
        detector=r'(?i)received a total',
        start=fr'[{CURRENCIES_SYMBOLS}]',
        end=r'\.$|\s',  # пробел не отработан
        required=True,
        ttype=float
    ),

    ParseTemplate(
        title=f'{TEMPLATES_TITLES["re_entry"]}',
        detector=r'(?i)re-entries',
        start=r'(?i)made ',
        end=r' ',
        required=False,
        ttype=int
    )
)
